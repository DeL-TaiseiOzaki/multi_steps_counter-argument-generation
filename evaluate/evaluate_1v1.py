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
    evaluation_index_path,
    evaluation_prompt_path
)
from utils.logging_config import setup_logging
from utils.file_handlers import load_evaluation_index, load_evaluation_prompts

from models.ai_models import get_ai_client
from evaluators.argument_evaluator_1v1 import evaluate_arguments

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

def prepare_counter_arguments(counterarguments, x1, x2):
    """指定された2つの反論を準備します"""
    counter_arguments_text = ""
    for i, x in enumerate([x1, x2], 1):
        if x in counterarguments:
            # 通常は 'counterargument' キーがあるはず
            cnt_arg = counterarguments[x].get('counterargument', '')
            if cnt_arg:
                counter_arguments_text += f"{i}. {cnt_arg}\n"
    return counter_arguments_text.strip()

def main():
    setup_logging()
    evaluation_criteria = load_evaluation_index(evaluation_index_path)
    evaluation_prompts = load_evaluation_prompts(evaluation_prompt_path)

    parser = argparse.ArgumentParser(description="Counter-Argument Evaluator for 1v1 Comparison")
    parser.add_argument("--input", type=str, required=True, help="Path to generated counterarguments JSON file")
    parser.add_argument("--output", type=str, default='evaluation_results.json', help="Path to output JSON file")
    parser.add_argument("--evaluation-model", type=str, default='gpt-4-0125-preview', help="Model to use for evaluation")
    parser.add_argument("--criteria-ids", nargs='+', type=int, required=True, help="IDs of evaluation criteria to use")
    parser.add_argument("--temperature", type=float, required=True, help="Temperature for evaluation")
    parser.add_argument("--max-tokens", type=int, required=True, help="Max tokens for evaluation")
    parser.add_argument("--x1", type=str, required=True, help="First counter-argument to compare (e.g., 'x1')")
    parser.add_argument("--x2", type=str, required=True, help="Second counter-argument to compare (e.g., 'x2')")
    args = parser.parse_args()

    # APIキーの設定
    os.environ['OPENAI_API_KEY'] = openai_api_key

    # 評価用のクライアントを取得
    eval_client = get_ai_client("openai", {'openai_api_key': openai_api_key})
    eval_model = args.evaluation_model

    # Ranking形式の評価基準のみを使用
    selected_criteria = [
        crit for crit in evaluation_criteria['evaluation_criteria'] 
        if crit['id'] in args.criteria_ids and crit['name'].startswith("(Ranking)")
    ]

    if not selected_criteria:
        logging.error(f"No valid ranking criteria matched the specified IDs: {args.criteria_ids}")
        sys.exit(1)

    generated_data = load_generated_data(args.input)
    results = []

    for item in generated_data:
        topic = item['topic']
        affirmative_argument = item['affirmative_argument']
        comparison_result = {
            'topic': topic,
            'x1': args.x1,
            'x2': args.x2,
            'evaluation_results': {}
        }

        # 各モデルについて評価を実行
        for model_name, counterarguments in item['counterarguments'].items():
            counter_arguments_text = prepare_counter_arguments(counterarguments, args.x1, args.x2)
            
            if not counter_arguments_text:
                logging.warning(f"Could not find both counter-arguments for model {model_name} on topic '{topic}'")
                continue

            try:
                evaluation_results = evaluate_arguments(
                    eval_client, eval_model, topic, affirmative_argument,
                    counter_arguments_text, selected_criteria, evaluation_prompts,
                    temperature=args.temperature, max_tokens=args.max_tokens
                )
                comparison_result['evaluation_results'][model_name] = evaluation_results
                print(f"Evaluation completed for model {model_name} on topic '{topic}'")
            except Exception as e:
                error_message = f"An error occurred during evaluation for model {model_name} on topic '{topic}': {e}"
                logging.error(error_message)

        results.append(comparison_result)

    # 結果を出力
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Evaluation results saved to {args.output}")

if __name__ == "__main__":
    main()