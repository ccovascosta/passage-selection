import json
import os
import sys
from datetime import datetime

def load_config(config_file='config.json'):
    if os.path.exists(config_file):
        with open(config_file, 'r') as file:
            config = json.load(file)
            return set_default_config(config)
    else:
        print(f"Configuration file '{config_file}' not found. Exiting.")
        sys.exit(1)

def serialize_metadata(metadata):
    if 'lastmodifiedtime' in metadata and metadata['lastmodifiedtime'] is not None:
        if isinstance(metadata['lastmodifiedtime'], datetime):
            metadata['lastmodifiedtime'] = metadata['lastmodifiedtime'].isoformat()
        else:
            metadata['lastmodifiedtime'] = str(metadata['lastmodifiedtime'])
    return metadata

def save_debug_json(doc_name, metadata, text, preprocessed_passages, folder='processed_folder'):
    os.makedirs(folder, exist_ok=True)
    metadata = serialize_metadata(metadata)
    debug_info = {
        'filename': metadata['filename'],
        'type': metadata['type'],
        'title': metadata['title'],
        'authors': metadata['authors'],
        'lastmodifiedtime': metadata['lastmodifiedtime'],
        'text': text,
    }
    with open(os.path.join(folder, f"{doc_name}.json"), 'w', encoding='utf-8') as file:
        json.dump(debug_info, file, indent=4)

def update_config(config, updates):
    config.update(updates)
    with open('config.json', 'w') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)
    return config

def set_default_config(config):
    default_config = {
        "document_folder_path": "sample_data",
        "query": "",
        "preprocess_query": False,
        "top_k_docs": 5,
        "top_n_passages": 3,
        "max_output_passages": 10,
        "passage_max_length": 512,
        "passage_overlap": 50,
        "split_method": "tokens",
        "retrieval_algorithm": "bm25",
        "ranking_method": "sentence_transformers",
        "output_file": "results.json"
    }
    for key, value in default_config.items():
        config.setdefault(key, value)
    return config
