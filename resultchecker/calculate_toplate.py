import json
import matplotlib.pyplot as plt
import numpy as np

def preprocess_ranking_data(data):
    cleaned_data = [item for item in data if item != 0]
    flattened_data = [0,0,0,0]
    for i,item in enumerate(cleaned_data):
        if isinstance(item, list):
            for subitem in item:
                flattened_data[subitem-4] = i+1
        elif isinstance(item, int):
            flattened_data[item-4] = i+1
    return flattened_data

def calculate_top_2_probability(rankings):
    top_2_counts = [0, 0, 0, 0]
    total_rankings = len(rankings)
    
    for ranking in rankings:
        processed_ranking = preprocess_ranking_data(ranking)
        for i, rank in enumerate(processed_ranking):
            if rank <= 2:
                top_2_counts[i] += 1
    
    probabilities = [count / total_rankings for count in top_2_counts]
    return probabilities

# JSONファイルからデータを読み込む
with open('resultchecker/fixed_evaluation_results_4-7.json', 'r') as file:
    data = json.load(file)

# すべてのレコードから評価結果を抽出
all_evaluation_results = {model: {6: [], 7: [], 8: []} for model in ['mini', 'gpt', 'llama', 'all']}
for record in data:
    for model, results in record['evaluation_results'].items():
        for result in results:
            all_evaluation_results[model][result['id']].append(result['result'])
            all_evaluation_results['all'][result['id']].append(result['result'])

# 各モデル、各評価指標の確率を計算
probabilities = {model: {} for model in ['mini', 'gpt', 'llama', 'all']}
for model in all_evaluation_results:
    for eval_id in all_evaluation_results[model]:
        probabilities[model][eval_id] = calculate_top_2_probability(all_evaluation_results[model][eval_id])

# 結果の可視化
fig, axs = plt.subplots(2, 2, figsize=(20, 16))
eval_names = {6: "Attacking a More Critical Premise", 
              7: "Attacking a More Implicit Premise", 
              8: "The Counter-Argument Is Overall Stronger"}
models = ['mini', 'gpt', 'llama', 'all']

for idx, (eval_id, eval_name) in enumerate(eval_names.items()):
    ax = axs[idx // 2, idx % 2]
    x = np.arange(len(models))
    width = 0.2

    for i in range(4):
        ax.bar(x + i*width, [probabilities[model][eval_id][i] for model in models], 
               width, label=f'x{i+4}')

    ax.set_ylabel('Probability of being in top 2')
    ax.set_title(f'{eval_name} (id: {eval_id})')
    ax.set_xticks(x + width * 1.5)
    ax.set_xticklabels(models)
    ax.legend(title='Arguments', loc='upper left', bbox_to_anchor=(1, 1))

# 空のサブプロットを削除
fig.delaxes(axs[1, 1])

plt.tight_layout()
plt.show()

# 各モデル、各評価指標の確率を出力
for model in probabilities:
    print(f"\n{model}:")
    for eval_id, probs in probabilities[model].items():
        print(f"  Evaluation {eval_id} ({eval_names[eval_id]}): {probs}")