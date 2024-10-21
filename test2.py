import json
import random

def process_and_shuffle_jsonl(input_file, output_file):
    data_list = []
    
    # ファイルを読み込み、データを処理してリストに追加
    with open(input_file, 'r', encoding='utf-8') as infile:
        for line in infile:
            data = json.loads(line)
            
            # 'final_output'キーがあれば'initial_answer'に変更
            if 'final_output' in data:
                data['initial_answer'] = data.pop('final_output')
            
            data_list.append(data)
    
    # データをシャッフル
    random.shuffle(data_list)
    
    # シャッフルされたデータを新しいファイルに書き込み
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for data in data_list:
            json.dump(data, outfile, ensure_ascii=False)
            outfile.write('\n')

# スクリプトを実行
if __name__ == "__main__":
    input_file = "generated_sets.jsonl"
    output_file = "output.jsonl"
    process_and_shuffle_jsonl(input_file, output_file)
    print(f"処理が完了しました。シャッフルされた結果は {output_file} に保存されています。")