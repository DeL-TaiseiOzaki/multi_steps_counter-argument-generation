import argparse
import json
import logging
import sys
import os

# プロジェクトのルートディレクトリをシステムパスに追加
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from config import (
    openai_api_key,
    groq_api_key,
    prompt_path,
    models
)
from utils.logging_config import setup_logging
from utils.file_handlers import load_prompts

from models.ai_models import get_ai_client
from generators.counterargument_generator import generate_counterargument

def load_input_data(file_path: str) -> list:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("Input JSON must be a list of dictionaries with 'topic', 'context', and 'id' keys")
        for item in data:
            if 'topic' not in item or 'context' not in item or 'id' not in item:
                raise ValueError("Each item in the input JSON must contain 'topic', 'context', and 'id' keys")
        return data
    except Exception as e:
        logging.error(f"Error loading input data from {file_path}: {e}")
        sys.exit(1)

def main():
    setup_logging()
    prompts = load_prompts(prompt_path)

    parser = argparse.ArgumentParser(description="Counter-Argument Generator")
    parser.add_argument("--models", nargs='+', required=True, help="AI models to use")
    parser.add_argument("--temperature", type=float, required=True, help="Temperature for generation")
    parser.add_argument("--max-tokens", type=int, required=True, help="Max tokens for generation")
    parser.add_argument("--conditions", nargs='+', required=True, help="Conditions to use (x1, x2, x3, x4, x5, x6, x7)")
    parser.add_argument("--input", type=str, required=True, help="Path to input JSON file")
    parser.add_argument("--output", type=str, default='generated_counterarguments.json', help="Path to output JSON file")
    parser.add_argument("--id-range", type=str, help="ID range to process (e.g., '1-3' or '2,4,6')")
    args = parser.parse_args()

    # APIキーの設定
    os.environ['OPENAI_API_KEY'] = openai_api_key
    os.environ['GROQ_API_KEY'] = groq_api_key

    for model_name in args.models:
        if model_name not in models:
            raise ValueError(f"Unsupported model: {model_name}")

    input_data = load_input_data(args.input)

    # ID範囲の処理
    if args.id_range:
        if '-' in args.id_range:
            start, end = map(int, args.id_range.split('-'))
            id_list = list(range(start, end + 1))
        else:
            id_list = list(map(int, args.id_range.split(',')))
    else:
        id_list = None

    all_results = []

    for input_item in input_data:
        item_id = input_item['id']
        
        if id_list and item_id not in id_list:
            continue

        topic = input_item['topic']
        affirmative_argument = input_item['context']

        print(f"Processing item with ID: {item_id}")

        result_item = {
            "id": item_id,
            'topic': topic,
            'affirmative_argument': affirmative_argument,
            'counterarguments': {}
        }

        for model_name in args.models:
            model_info = models[model_name]
            client = get_ai_client(model_info['client_type'], {
                'openai_api_key': openai_api_key,
                'groq_api_key': groq_api_key
            })

            counterarguments = {}
            for condition in args.conditions:
                if condition not in ["x1", "x2", "x3", "x4", "x5", "x6", "x7"]:
                    logging.warning(f"Skipping invalid condition: {condition}")
                    continue

                print(f"Generating counterargument using {model_name} with condition {condition} for topic '{topic}' (ID: {item_id})...")

                try:
                    result = generate_counterargument(
                        client, topic, affirmative_argument, prompts,
                        model_info['model'], args.temperature, args.max_tokens, condition
                    )
                    counterarguments[condition] = {
                        "counterargument": result["counterargument"],
                        "steps": result["steps"]
                    }
                    print(f"Successfully generated counterargument for condition {condition} using model {model_name}")
                except Exception as e:
                    error_message = f"An error occurred for condition {condition} using model {model_name}: {e}\n"
                    logging.error(error_message)

            result_item['counterarguments'][model_name] = counterarguments

        all_results.append(result_item)

    # 結果を出力
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    print(f"Generated counterarguments saved to {args.output}")

if __name__ == "__main__":
    main()