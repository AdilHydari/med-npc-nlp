import torch
from transformers import BertTokenizer, BertForTokenClassification, pipeline

# Load BioBERT model and tokenizer
try:
    model_name = "dmis-lab/biobert-v1.1"
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertForTokenClassification.from_pretrained(model_name)
except Exception as e:
    raise RuntimeError(f"Error loading model or tokenizer: {e}")

# Create a pipeline for NER
try:
    nlp = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")
except Exception as e:
    raise RuntimeError(f"Error creating NLP pipeline: {e}")

def extract_symptoms(text):
    """
    Extracts symptoms from the given text using a named entity recognition (NER) pipeline.

    Args:
        text (str): The input text containing potential symptoms.

    Returns:
        list: A list of symptoms extracted from the text.
    """
    try:
        ner_results = nlp(text)
        symptoms = [result['word'] for result in ner_results if result['entity_group'] == 'DISEASE']
        return symptoms
    except Exception as e:
        raise RuntimeError(f"Error extracting symptoms: {e}")

# Testing the function
if __name__ == "__main__":
    sample_text = "I have a headache and feel dizzy."
    symptoms = extract_symptoms(sample_text)
    print(symptoms)
