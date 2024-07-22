import json
import logging

def load_prompts(file_path: str) -> dict:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading prompts from {file_path}: {e}")
        raise
