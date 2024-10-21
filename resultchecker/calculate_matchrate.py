import json
import pandas as pd
import numpy as np
from irrCAC.raw import CAC
import pingouin as pg

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

def calculate_agreement_irrCAC(data):
    data_df = pd.DataFrame(data).T
    print(data_df)
    cac = CAC(data_df)
    
    gwet_result = cac.gwet()

    melted_data = data_df.melt(var_name='raters', value_name='ratings')
    melted_data['targets'] = np.tile(np.arange(len(data_df)), len(data_df.columns))
    icc_result = pg.intraclass_corr(data=melted_data, targets='targets', raters='raters', ratings='ratings')
    icc_value = icc_result.set_index('Type').loc['ICC2', 'ICC']

    return {
        "Gwet's AC1": gwet_result['est']['coefficient_value']
    }

def analyze_model_agreement(data):
    model_data = {model: [] for model in ['mini', 'gpt', 'llama']}

    for item in data:
        eval_results = item.get('evaluation_results', {})
        for model in ['mini', 'gpt', 'llama']:
            model_results = eval_results.get(model, [])
            for ranking in model_results:
                result = ranking.get('result', [])
                preprocessed_result = preprocess_ranking_data(result)
                model_data[model].extend(preprocessed_result)
    data = []
    for model, rankings in model_data.items():
        data.append(rankings)
    
    print(calculate_agreement_irrCAC(data))
              
    return {model: calculate_agreement_irrCAC(rankings) for model, rankings in model_data.items()}


# JSONデータの読み込み
with open('resultchecker/fixed_evaluation_results_4-7.json', 'r') as file:
    data = json.load(file)

# 分析の実行
results = analyze_model_agreement(data)

# 結果の表示
for model, agreement in results.items():
    print(f"\nAgreement for {model.upper()} model:")
    for metric, value in agreement.items():
        print(f"{metric}: {value:.4f}")