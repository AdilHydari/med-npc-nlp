from datasets import load_dataset

# Load the MedQuAD dataset
dataset = load_dataset('medquad')

from transformers import BertTokenizer

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

def tokenize_function(examples):
    return tokenizer(examples['question'], padding='max_length', truncation=True)

tokenized_datasets = dataset.map(tokenize_function, batched=True)
tokenized_datasets = tokenized_datasets.rename_column("label", "labels")
tokenized_datasets.set_format('torch', columns=['input_ids', 'attention_mask', 'labels'])
import torch
import torch.nn as nn
from torch.nn import functional as F

class MultiHeadAttention(nn.Module):
    def __init__(self, embed_size, heads):
        super(MultiHeadAttention, self).__init__()
        self.embed_size = embed_size
        self.heads = heads
        self.head_dim = embed_size // heads

        assert (
            self.head_dim * heads == embed_size
        ), "Embedding size needs to be divisible by heads"

        self.values = nn.Linear(self.head_dim, self.head_dim, bias=False)
        self.keys = nn.Linear(self.head_dim, self.head_dim, bias=False)
        self.queries = nn.Linear(self.head_dim, self.head_dim, bias=False)
        self.fc_out = nn.Linear(heads * self.head_dim, embed_size)

    def forward(self, values, keys, query, mask):
        N = query.shape[0]

        value_len, key_len, query_len = values.shape[1], keys.shape[1], query.shape[1]

        # Split the embedding into self.heads different pieces
        values = values.reshape(N, value_len, self.heads, self.head_dim)
        keys = keys.reshape(N, key_len, self.heads, self.head_dim)
        queries = query.reshape(N, query_len, self.heads, self.head_dim)

        values = self.values(values)
        keys = self.keys(keys)
        queries = self.queries(queries)

        energy = torch.einsum("nqhd,nkhd->nhqk", [queries, keys])

        if mask is not None:
            energy = energy.masked_fill(mask == 0, float("-1e20"))

        attention = torch.softmax(energy / (self.embed_size ** (1 / 2)), dim=3)

        out = torch.einsum("nhql,nlhd->nqhd", [attention, values]).reshape(
            N, query_len, self.heads * self.head_dim
        )

        out = self.fc_out(out)
        return out

class gMLPBlock(nn.Module):
    def __init__(self, embed_size, hidden_size):
        super(gMLPBlock, self).__init__()
        self.fc1 = nn.Linear(embed_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, embed_size)
        self.activation = nn.GELU()

    def forward(self, x):
        out = self.fc1(x)
        out = self.activation(out)
        out = self.fc2(out)
        return out

class CustomGMLP(nn.Module):
    def __init__(self, embed_size, hidden_size, heads, num_classes):
        super(CustomGMLP, self).__init__()
        self.attention = MultiHeadAttention(embed_size, heads)
        self.gmlp = gMLPBlock(embed_size, hidden_size)
        self.fc_out = nn.Linear(embed_size, num_classes)
        self.dropout = nn.Dropout(0.3)
        self.embed_size = embed_size

    def forward(self, x, mask):
        attn_output = self.attention(x, x, x, mask)
        gmlp_output = self.gmlp(attn_output)
        out = self.fc_out(self.dropout(gmlp_output[:, 0, :]))
        return out

# Model hyperparameters
embed_size = 768
hidden_size = 3072
heads = 12
num_classes = 2  # Assuming binary classification for sentiment analysis

model = CustomGMLP(embed_size, hidden_size, heads, num_classes)
class CustomGMLPSentimentAnalyzer:
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer

    def analyze_sentiment(self, text):
        inputs = self.tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)
        mask = inputs['attention_mask']
        outputs = self.model(inputs['input_ids'], mask)
        probs = F.softmax(outputs, dim=-1)
        sentiment = torch.argmax(probs).item()
        return sentiment

# Example usage
analyzer = CustomGMLPSentimentAnalyzer(model, tokenizer)
sentiment = analyzer.analyze_sentiment("I'm feeling great about this diagnosis!")
print(f"Sentiment: {'Positive' if sentiment == 1 else 'Negative'}")
