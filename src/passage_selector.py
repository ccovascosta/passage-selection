import os
import json
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_ingestion import load_document
from src.preprocess import preprocess_text, split_text_into_passages
from src.query_processing import process_query
from src.document_retrieval import retrieve_documents
from src.passage_extraction import extract_relevant_passages
from src.utils import save_debug_json

def run_pipeline(config, debug=False):
    document_folder_path = config['document_folder_path']
    query = config['query']
    preprocess_query = config['preprocess_query']
    top_k_docs = config['top_k_docs']
    top_n_passages = config['top_n_passages']
    max_output_passages = config['max_output_passages']
    passage_max_length = config['passage_max_length']
    passage_overlap = config['passage_overlap']
    split_method = config['split_method']
    retrieval_algorithm = config['retrieval_algorithm']
    ranking_method = config['ranking_method']
    output_file = config['output_file']

    if preprocess_query:
        query = process_query(query)

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

    top_documents = retrieve_documents(query, documents, top_k_docs, algorithm=retrieval_algorithm, debug=debug)

    if debug:
        print("Extracting relevant passages from the top documents")

    relevant_passages = []

    for metadata, _, original_passages, preprocessed_passages in top_documents:
        doc_name = metadata['filename']

        if debug:
            print(f"Extracting passages from document: {doc_name}")

        passages = extract_relevant_passages(query, doc_name, original_passages, preprocessed_passages, top_n_passages, method=ranking_method)
        relevant_passages.extend(passages)

    n_output_passages = min(top_n_passages * top_k_docs, max_output_passages)
    relevant_passages = sorted(relevant_passages, key=lambda x: x[2], reverse=True)[:n_output_passages]

    if debug:
        output_data = {
            "query": query,
            "results": [
                {
                    "document": passage[0],
                    "passage": passage[1],
                    "score": passage[2]
                } for passage in relevant_passages
            ]
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=4)

        print(f"Results have been written to {output_file}")

    return query, relevant_passages
