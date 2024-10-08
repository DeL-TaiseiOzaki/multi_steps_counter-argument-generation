import argparse
import json
import logging
import sys
import os
from config import (
    openai_api_key,
    evaluation_index_path,
    evaluation_prompt_path
)
from utils.logging_config import setup_logging
from utils.file_handlers import load_evaluation_index, load_evaluation_prompts

from models.ai_models import get_ai_client
from evaluators.argument_evaluator import evaluate_arguments

def load_generated_data(file_path: str) -> list:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("Generated data JSON must be a list")
        return data
    except Exception as e:
        logging.error(f"Error loading generated data from {file_path}: {e}")
        sys.exit(1)

def main():
    setup_logging()
    evaluation_criteria = load_evaluation_index(evaluation_index_path)
    evaluation_prompts = load_evaluation_prompts(evaluation_prompt_path)

    parser = argparse.ArgumentParser(description="Counter-Argument Evaluator")
    parser.add_argument("--input", type=str, required=True, help="Path to generated counterarguments JSON file")
    parser.add_argument("--output", type=str, default='evaluation_results.json', help="Path to output JSON file")
    parser.add_argument("--evaluation-model", type=str, default='gpt-4o-2024-08-06', help="Model to use for evaluation")
    parser.add_argument("--criteria-ids", nargs='+', type=int, required=True, help="IDs of evaluation criteria to use")
    parser.add_argument("--temperature", type=float, required=True, help="Temperature for evaluation")
    parser.add_argument("--max-tokens", type=int, required=True, help="Max tokens for evaluation")
    args = parser.parse_args()

    # APIキーの設定
    os.environ['OPENAI_API_KEY'] = openai_api_key

    # 評価用のクライアントを取得
    eval_client = get_ai_client("openai", {'openai_api_key': openai_api_key})
    eval_model = args.evaluation_model

    # 指定された評価指標のみを使用
    selected_criteria = [crit for crit in evaluation_criteria['evaluation_criteria'] if crit['id'] in args.criteria_ids]

    if not selected_criteria:
        logging.error(f"No evaluation criteria matched the specified IDs: {args.criteria_ids}")
        sys.exit(1)

    generated_data = load_generated_data(args.input)

    for item in generated_data:
        topic = item['topic']
        affirmative_argument = item['affirmative_argument']
        item['evaluation_results'] = {}

        # 各モデルについて評価を実行
        for model_name, counterarguments in item['counterarguments'].items():
            counter_arguments_text = ""
            for idx, (cond, cnt_arg) in enumerate(counterarguments.items(), start=1):
                counter_arguments_text += f"{idx}. {cnt_arg}\n"

            if counter_arguments_text.strip() == "":
                logging.warning(f"No counterarguments to evaluate for model {model_name} on topic '{topic}'")
                continue

            try:
                evaluation_results = evaluate_arguments(
                    eval_client, eval_model, topic, affirmative_argument,
                    counter_arguments_text, selected_criteria, evaluation_prompts,
                    temperature=args.temperature, max_tokens=args.max_tokens
                )
                item['evaluation_results'][model_name] = evaluation_results
                print(f"Evaluation completed for model {model_name} on topic '{topic}'")
            except Exception as e:
                error_message = f"An error occurred during evaluation for model {model_name} on topic '{topic}': {e}\n"
                logging.error(error_message)

    # 結果を出力
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(generated_data, f, ensure_ascii=False, indent=2)
    print(f"Evaluation results saved to {args.output}")

if __name__ == "__main__":
    main()
