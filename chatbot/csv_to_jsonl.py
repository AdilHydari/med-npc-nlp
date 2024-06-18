import csv
import json

def csv_to_jsonl(csv_file_path, jsonl_file_path):
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        
        with open(jsonl_file_path, 'w', encoding='utf-8') as jsonl_file:
            for row in reader:
                jsonl_file.write(json.dumps(row) + '\n')

if __name__ == "__main__":
    csv_file_path = 'All-2479-Answers-retrieved-from-MedQuAD.csv'  # Replace with your CSV file path
    jsonl_file_path = 'All-2479-Answers-retrieved-from-MedQuAD.jsonl'  # Replace with your desired JSONL file path
    
    csv_to_jsonl(csv_file_path, jsonl_file_path)
    print(f"CSV file '{csv_file_path}' has been converted to JSONL file '{jsonl_file_path}'")
