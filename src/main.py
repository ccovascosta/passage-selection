import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_ingestion import load_documents
from src.preprocess import preprocess_text
from src.query_processing import process_query
from src.document_retrieval import retrieve_documents
from src.passage_extraction import extract_relevant_passages

def read_config(config_file='config.json'):
    if os.path.exists(config_file):
        with open(config_file, 'r') as file:
            config = json.load(file)
            return config
    else:
        print(f"Configuration file '{config_file}' not found. Exiting.")
        sys.exit(1)

def save_debug_json(doc_name, metadata, text, preprocessed_text, folder='debug_json'):
    os.makedirs(folder, exist_ok=True)
    debug_info = {
        'filename': metadata['filename'],
        'type': metadata['type'],
        'title': metadata['title'],
        'authors': metadata['authors'],
        'lastmodifiedtime': metadata['lastmodifiedtime'],
        'text': text,
        'preprocessed_text': preprocessed_text
    }
    with open(os.path.join(folder, f"{doc_name}.json"), 'w', encoding='utf-8') as file:
        json.dump(debug_info, file, indent=4)

def main(config_file='config.json', document_folder_path=None, query_text=None, top_k=None, passage_max_length=None, passage_overlap=None, split_method=None, debug=True):
    config = read_config(config_file)
    
    document_folder_path = document_folder_path or config.get('document_folder_path') or input("Enter the folder path containing documents: ")
    query_text = query_text or config.get('query_text') or input("Enter the query/utterance: ")
    top_k = top_k or config.get('top_k', 5)
    passage_max_length = passage_max_length or config.get('passage_max_length', 512)
    passage_overlap = passage_overlap or config.get('passage_overlap', 50)
    split_method = split_method or config.get('split_method', 'tokens')

    documents = load_documents(document_folder_path)
    preprocessed_documents = [(name, preprocess_text(text)) for name, text in documents]

    if debug:
        for name, text, metadata in preprocessed_documents:
            preprocessed_text = preprocess_text(text)
            save_debug_json(name, metadata, text, preprocessed_text)

    query = process_query(query_text)
    top_documents = retrieve_documents(query, preprocessed_documents, top_k)
    relevant_passages = extract_relevant_passages(query, top_documents, passage_max_length, passage_overlap, split_method)
    return relevant_passages

if __name__ == "__main__":
    results = main()
    for result in results:
        print(f"Document: {result[0]}\nPassage: {result[1]}\nScore: {result[2]}\n")
