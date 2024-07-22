from openai import OpenAI
from groq import Groq

def get_ai_client(client_type: str, config: dict):
    if client_type == "openai":
        return OpenAI(api_key=config['openai_api_key'])
    elif client_type == "groq":
        return Groq(api_key=config['groq_api_key'])
    else:
        raise ValueError(f"Unsupported client type: {client_type}")