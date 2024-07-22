import argparse
import json
import logging
import sys
from config import load_config
from utils.logging_config import setup_logging
from utils.file_handlers import load_prompts

try:
    from models.ai_models import get_ai_client
except ImportError as e:
    logging.error(f"Error importing AI models: {e}")
    logging.error("Please make sure all required libraries are installed.")
    logging.error("You may need to run: pip install -r requirements.txt")
    sys.exit(1)

from generators.counterargument_generator import generate_counterargument

def load_input_data(file_path: str) -> dict:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if 'topic' not in data or 'affirmative-argument' not in data:
            raise ValueError("Input JSON must contain 'topic' and 'affirmative-argument' keys")
        return data
    except Exception as e:
        logging.error(f"Error loading input data from {file_path}: {e}")
        sys.exit(1)

def write_output(output: str, file_path: str):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"Output written to {file_path}")
    except Exception as e:
        logging.error(f"Error writing output to {file_path}: {e}")

def main():
    setup_logging()
    config = load_config()
    prompts = load_prompts(config['prompt_path'])

    parser = argparse.ArgumentParser(description="Counter-Argument Generator")
    parser.add_argument("--model", type=str, required=True, help="AI model to use")
    parser.add_argument("--temperature", type=float, required=True, help="Temperature for generation")
    parser.add_argument("--max-tokens", type=int, required=True, help="Max tokens for generation")
    parser.add_argument("--conditions", nargs='+', required=True, help="Conditions to use (x1, x2, x3, x4)")
    parser.add_argument("--input", type=str, required=True, help="Path to input JSON file")
    parser.add_argument("--output", type=str, choices=['print', 'file'], default='print', help="Output method: print to console or save to file")
    parser.add_argument("--output-file", type=str, help="Path to output file (required if --output=file)")
    args = parser.parse_args()

    if args.output == 'file' and not args.output_file:
        parser.error("--output-file is required when --output is set to 'file'")

    if args.model not in config['models']:
        raise ValueError(f"Unsupported model: {args.model}")

    model_info = config['models'][args.model]
    client = get_ai_client(model_info['client_type'], config)

    input_data = load_input_data(args.input)
    topic = input_data['topic']
    affirmative_argument = input_data['affirmative-argument']

    output = ""
    for condition in args.conditions:
        if condition not in ["x1", "x2", "x3", "x4"]:
            logging.warning(f"Skipping invalid condition: {condition}")
            continue

        print(f"Generating counterargument using {args.model} with condition {condition}...")
        
        try:
            counterargument = generate_counterargument(
                client, topic, affirmative_argument, prompts,
                model_info['model'], args.temperature, args.max_tokens, condition
            )
            result = f"\nGenerated Counterargument for condition {condition}:\n{counterargument}\n"
            
            if args.output == 'print':
                print(result)
            output += result
            print(f"Successfully generated counterargument for condition {condition}")
        except Exception as e:
            error_message = f"An error occurred for condition {condition}: {e}\n"
            logging.error(error_message)
            if args.output == 'print':
                print(error_message)
            output += error_message

    if args.output == 'file':
        write_output(output, args.output_file)

if __name__ == "__main__":
    main()