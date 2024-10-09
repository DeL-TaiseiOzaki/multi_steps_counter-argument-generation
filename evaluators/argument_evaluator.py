import logging
from typing import List, Dict
from models.ai_models import get_ai_client
from utils.file_handlers import load_evaluation_prompts

def analyze_debate(client, model, topic, affirmative_argument, counter_arguments, prompts, temperature=0, max_tokens=1000):
    """ディベートを分析します。"""
    system_prompt_template = prompts['system_prompt_template']
    analysis_user_prompt = prompts['analysis_user_prompt']

    system_prompt = system_prompt_template.format(
        topic=topic,
        affirmative_argument=affirmative_argument,
        counter_arguments=counter_arguments
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": analysis_user_prompt}
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content

def evaluate_selection(client, model, topic, affirmative_argument, counter_arguments, selection_criteria, criteria_description, analysis, prompts, temperature=0, max_tokens=1000):
    """選択式の評価を行います。"""
    selection_user_prompt_template = prompts['selection_user_prompt_template']

    selection_prompt = selection_user_prompt_template.format(
        selection_criteria=selection_criteria,
        criteria_description=criteria_description
    )

    messages = [
        {"role": "assistant", "content": analysis},
        {"role": "user", "content": selection_prompt}
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content

def evaluate_ranking(client, model, topic, affirmative_argument, counter_arguments, ranking_criteria, criteria_description, analysis, prompts, temperature=0, max_tokens=1000):
    """ランキング式の評価を行います。"""
    ranking_user_prompt_template = prompts['ranking_user_prompt_template']

    ranking_prompt = ranking_user_prompt_template.format(
        ranking_criteria=ranking_criteria,
        criteria_description=criteria_description
    )

    messages = [
        {"role": "assistant", "content": analysis},
        {"role": "user", "content": ranking_prompt}
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content

def evaluate_arguments(client, model, topic, affirmative_argument, counter_arguments, evaluation_criteria, prompts, temperature=0, max_tokens=1000):
    """指定された評価指標のみを使用して評価を行います。"""
    analysis = analyze_debate(client, model, topic, affirmative_argument, counter_arguments, prompts, temperature, max_tokens)
    results = []

    for item in evaluation_criteria:
        id = item['id']
        name = item['name']
        description = item['description']

        result = {"id": id, "name": name}

        if name.startswith("(Multiple Choice)"):
            selection_criteria = name
            criteria_description = description
            selection_results = evaluate_selection(client, model, topic, affirmative_argument, counter_arguments, selection_criteria, criteria_description, analysis, prompts, temperature, max_tokens)
            logging.info(f"Selection results for item {id}: {selection_results}")
            result["result"] = selection_results
        elif name.startswith("(Ranking)"):
            ranking_criteria = name
            criteria_description = description
            ranking_results = evaluate_ranking(client, model, topic, affirmative_argument, counter_arguments, ranking_criteria, criteria_description, analysis, prompts, temperature, max_tokens)
            logging.info(f"Ranking results for item {id}: {ranking_results}")
            result["result"] = ranking_results
        else:
            logging.warning(f"Unknown evaluation type for item {id}: {name}")
            result["result"] = []

        results.append(result)

    return results