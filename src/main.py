import os
import sys
import nltk
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_ingestion import load_document
from src.preprocess import preprocess_text, split_text_into_passages
from src.query_processing import process_query
from src.document_retrieval import retrieve_documents
from src.passage_extraction import extract_relevant_passages
from src.utils import read_config, save_debug_json

nltk.download('stopwords')

def main(debug=False):
    config = read_config()

    document_folder_path = config.get('document_folder_path') or input("Enter the folder path containing documents: ")
    query_text = config.get('query_text') or input("Enter the query/utterance: ")
    top_k_docs = config.get('top_k_docs', 5)
    top_n_passages = config.get('top_n_passages', 2)
    passage_max_length = config.get('passage_max_length', 512)
    passage_overlap = config.get('passage_overlap', 'tokens')
    split_method = config.get('split_method', 'tokens')

    query = process_query(query_text)

    documents = []

    for file_name in os.listdir(document_folder_path):
        file_path = os.path.join(document_folder_path, file_name)
        if debug:
            print(f"Reading document: {file_name}")
        text, metadata = load_document(file_path)
        if text is None:
            continue

        if debug:
            print(f"Preprocessing document: {file_name}")

        preprocessed_text = preprocess_text(text)

        original_passages = split_text_into_passages(text, passage_max_length, passage_overlap, split_method)
        preprocessed_passages = [preprocess_text(passage) for passage in original_passages]

        documents.append((metadata, preprocessed_text, original_passages, preprocessed_passages))

        if debug:
            save_debug_json(metadata['filename'], metadata, text, preprocessed_passages)

    if debug:
        print("All documents have been processed.")
        print(f"Evaluating the top {top_k_docs} most relevant documents")

    top_documents = retrieve_documents(query, documents, top_k_docs, debug=debug)

    if debug:
        print("Extracting relevant passages from the top documents")

    relevant_passages = []

    for metadata, _, original_passages, preprocessed_passages in top_documents:
        doc_name = metadata['filename']

        if debug:
            print(f"Extracting passages from document: {doc_name}")

        passages = extract_relevant_passages(query, doc_name, original_passages, preprocessed_passages, top_n_passages)
        relevant_passages.extend(passages)
        if debug:
            for passage in passages:
                print(f"Document: {passage[0]}\nPassage: {passage[1]}\nScore: {passage[2]}\n")

    if debug:
        output_file = config.get('output_file', 'results.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(relevant_passages, f, ensure_ascii=False, indent=4)

        print(f"Results have been written to {output_file}")

    return relevant_passages

if __name__ == "__main__":
    debug_mode = True
    results = main(debug=debug_mode)
    for result in results:
        print(f"Document: {result[0]}\nPassage: {result[1]}\nScore: {result[2]}\n")
