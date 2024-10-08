import json
import logging

def load_prompts(file_path: str) -> dict:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading prompts from {file_path}: {e}")
        raise

def load_evaluation_index(file_path: str) -> dict:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading evaluation index from {file_path}: {e}")
        raise

def load_evaluation_prompts(file_path: str) -> dict:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading evaluation prompts from {file_path}: {e}")
        raise
