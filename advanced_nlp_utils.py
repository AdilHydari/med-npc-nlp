import torch
from transformers import BertTokenizer, BertForTokenClassification
from transformers import pipeline

# Load BioBERT model and tokenizer
model_name = "dmis-lab/biobert-v1.1"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForTokenClassification.from_pretrained(model_name)

# Create a pipeline for NER
nlp = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

def extract_symptoms(text):
    ner_results = nlp(text)
    symptoms = [result['word'] for result in ner_results if result['entity_group'] == 'DISEASE']
    return symptoms

# Testing the function
if __name__ == "__main__":
    sample_text = "I have a headache and feel dizzy."
    symptoms = extract_symptoms(sample_text)
    print(symptoms)
