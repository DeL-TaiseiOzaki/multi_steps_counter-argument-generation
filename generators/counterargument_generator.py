import logging
from typing import List, Dict

def generate_response(client, messages: List[Dict], model: str, temperature: float, max_tokens: int) -> str:
    try:
        if hasattr(client, 'chat'):
            chat_completion = client.chat.completions.create(
                messages=messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        else:
            chat_completion = client.completions.create(
                model=model,
                prompt=messages[-1]['content'],
                temperature=temperature,
                max_tokens=max_tokens
            )
        return chat_completion.choices[0].message.content if hasattr(chat_completion.choices[0], 'message') else chat_completion.choices[0].text
    except Exception as e:
        logging.error(f"Error generating response: {e}")
        raise

def extract_premise(affirmative_argument: str) -> str:
    premise_list = affirmative_argument.split(".")
    combined_premises_text = "\n".join(f"{i+1}.{premise.strip()}" for i, premise in enumerate(premise_list) if premise.strip())
    return combined_premises_text

def generate_counterargument(client, topic: str, affirmative_argument: str, prompts: Dict, model: str, temperature: float, max_tokens: int, condition: str) -> str:
    conversation_history = [
        {"role": "system", "content": prompts["system_prompt"]}
    ]

    try:
        premise_list = extract_premise(affirmative_argument)
        
        if condition == "x1":
            premise_prompt = prompts["x1"]["premise_generation_prompt"].replace("#topic#", topic).replace("#argument#", affirmative_argument)
            conversation_history.append({"role": "user", "content": premise_prompt})
            generated_premise_list = generate_response(client, conversation_history, model, temperature, max_tokens)
            conversation_history.append({"role": "assistant", "content": generated_premise_list})

            decision_prompt = prompts["x1"]["premise_decision_prompt"]
            conversation_history.append({"role": "user", "content": decision_prompt})
            chosen_premise = generate_response(client, conversation_history, model, temperature, max_tokens)
            conversation_history.append({"role": "assistant", "content": chosen_premise})

            counterargument_prompt = prompts["x1"]["counter-argument_generation_prompt"]
            conversation_history.append({"role": "user", "content": counterargument_prompt})

        elif condition in ["x2", "x3"]:
            decision_prompt = prompts[condition]["premise_decision_prompt"].replace("#topic#", topic).replace("#argument#", affirmative_argument).replace("###premise_list###", premise_list)
            conversation_history.append({"role": "user", "content": decision_prompt})
            chosen_premise = generate_response(client, conversation_history, model, temperature, max_tokens)
            conversation_history.append({"role": "assistant", "content": chosen_premise})

            counterargument_prompt = prompts[condition]["counter-argument_generation_prompt"]
            conversation_history.append({"role": "user", "content": counterargument_prompt})

        elif condition in ["x4", "x6"]:
            counterargument_prompt = prompts[condition]["counter-argument_generation_prompt"].replace("#topic#", topic).replace("#argument#", affirmative_argument)
            conversation_history.append({"role": "user", "content": counterargument_prompt})

        elif condition == "x5":
            counterargument_prompt = prompts[condition]["counter-argument_generation_prompt"].replace("#topic#", topic).replace("#argument#", affirmative_argument).replace("###premise_list###", premise_list)
            conversation_history.append({"role": "user", "content": counterargument_prompt})

        else:
            raise ValueError(f"Invalid condition: {condition}")

        counterargument = generate_response(client, conversation_history, model, temperature, max_tokens)
        return counterargument

    except Exception as e:
        logging.error(f"Error generating counterargument: {e}")
        raise