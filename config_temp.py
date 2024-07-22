import os

def load_config():
    return {
        'openai_api_key': os.environ.get('OPENAI_API_KEY', 'your_openai_api_key_here'),
        'groq_api_key': os.environ.get('GROQ_API_KEY', 'your_groq_api_key_here'),
        'prompt_path': 'path/to/your/prompts.json',
        'models': {
            "gpt-3.5-turbo": {"client_type": "openai", "model": "gpt-3.5-turbo"},
            "gpt-4": {"client_type": "openai", "model": "gpt-4"},
            "llama3-70b": {"client_type": "groq", "model": "llama3-70b-8192"}
        }
    }