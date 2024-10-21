import json
import ast
import re

def parse_ranking(ranking_str):
    # コードブロックを除去
    ranking_str = ranking_str.strip('`').strip()
    if ranking_str.startswith('python'):
        ranking_str = re.sub(r'^python\s*\n', '', ranking_str)
    
    # 空白文字を除去
    ranking_str = re.sub(r'\s+', '', ranking_str)
    
    try:
        # まずPythonのリテラルとして評価を試みる
        return ast.literal_eval(ranking_str)
    except:
        try:
            # 次に、数字とカンマ、括弧のみを含む文字列として解析
            clean_str = re.sub(r'[^\d,\[\]]', '', ranking_str)
            return json.loads(clean_str)
        except:
            # 最後の手段として、数字のみを抽出してリストに変換
            return [int(x) for x in re.findall(r'\d+', ranking_str)]

def process_evaluation_results(data):
    for topic in data:
        for model, results in topic['evaluation_results'].items():
            for result in results:
                result['result'] = parse_ranking(result['result'])
    return data

def verify_list_conversion(data):
    all_converted = True
    for topic in data:
        for model, results in topic['evaluation_results'].items():
            for result in results:
                if not isinstance(result['result'], list):
                    print(f"警告: topic {topic['id']}, model {model}, result {result['id']} はリストに変換されていません。")
                    all_converted = False
    return all_converted

# JSONファイルを読み込む
with open('/workspaces/multi_steps_counter-argument-generation/evaluation_results_4-7.json', 'r') as f:
    data = json.load(f)

# データを処理
processed_data = process_evaluation_results(data)

# 変換を確認
if verify_list_conversion(processed_data):
    print("すべての評価結果が正常にリストに変換されました。")
else:
    print("一部の評価結果がリストに変換されていません。上記の警告を確認してください。")

# 処理したデータを新しいJSONファイルに書き込む
with open('resultchecker/fixed_evaluation_results_4-7.json', 'w') as f:
    json.dump(processed_data, f, indent=2)