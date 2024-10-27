import logging
from typing import List, Dict
from models.ai_models import get_ai_client

def evaluate_ranking(client, model, topic, affirmative_argument, counter_arguments, ranking_criteria, criteria_description, prompts, temperature=0, max_tokens=1000):
    """ランキング式の評価を行います。"""
    system_prompt_template = prompts['system_prompt_template']
    ranking_user_prompt_template = prompts['ranking_user_prompt_template']

    # システムプロンプトの準備
    system_prompt = system_prompt_template.format(
        topic=topic,
        affirmative_argument=affirmative_argument,
        counter_arguments=counter_arguments
    )

    # ランキングプロンプトの準備
    ranking_prompt = ranking_user_prompt_template.format(
        ranking_criteria=ranking_criteria,
        criteria_description=criteria_description
    )

    messages = [
        {"role": "system", "content": system_prompt},
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
    """指定された評価指標に基づいて評価を行います。"""
    results = []

    for item in evaluation_criteria:
        id = item['id']
        name = item['name']
        description = item['description']

        result = {"id": id, "name": name}

        if name.startswith("(Ranking)"):
            ranking_criteria = name
            criteria_description = description
            ranking_results = evaluate_ranking(
                client, model, topic, affirmative_argument, 
                counter_arguments, ranking_criteria, criteria_description, 
                prompts, temperature, max_tokens
            )
            logging.info(f"Ranking results for item {id}: {ranking_results}")
            result["result"] = ranking_results
        else:
            logging.warning(f"Unsupported evaluation type for item {id}: {name}")
            result["result"] = []

        results.append(result)

    return results