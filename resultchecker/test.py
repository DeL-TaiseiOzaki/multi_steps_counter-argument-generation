import json

# JSONファイルのパス
file_path = 'resultchecker/fixed_evaluation_results_4-7.json'

# JSONファイルを読み込む
try:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
except FileNotFoundError:
    print(f"ファイル '{file_path}' が見つかりません。パスを確認してください。")
    exit()
except json.JSONDecodeError:
    print(f"ファイル '{file_path}' のJSON形式に誤りがあります。")
    exit()

# 各モデルの評価結果が3つずつ存在するか確認
models = ['mini', 'gpt', 'llama']
expected_count = 3

# データがリストであることを確認
if not isinstance(data, list):
    print("データの形式が正しくありません。リスト形式である必要があります。")
    exit()

# 各アイテムについて検証
for item in data:
    # 各アイテムの識別子を取得（存在しない場合は 'Unknown ID'）
    item_id = item.get('id', 'Unknown ID')
    
    # 'evaluation_results' キーが存在するか確認
    if 'evaluation_results' not in item:
        print(f"アイテムID {item_id}: 'evaluation_results' キーが存在しません。")
        continue
    
    evaluation_results = item['evaluation_results']
    
    # 各モデルについてチェック
    for model in models:
        if model not in evaluation_results:
            print(f"アイテムID {item_id}: モデル '{model}' の評価結果が存在しません。")
            continue
        
        actual_count = len(evaluation_results[model])
        
        if actual_count == expected_count:
            print(f"アイテムID {item_id}: モデル '{model}' は期待通りに {expected_count} つの結果を持っています。")
        else:
            print(f"アイテムID {item_id}: モデル '{model}' の結果数が期待と異なります。期待: {expected_count}, 実際: {actual_count}")
