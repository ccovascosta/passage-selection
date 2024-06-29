import json
import os
import sys
from datetime import datetime

def read_config(config_file='config.json'):
    if os.path.exists(config_file):
        with open(config_file, 'r') as file:
            config = json.load(file)
            return config
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
