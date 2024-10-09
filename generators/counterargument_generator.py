import logging
from typing import List, Dict

def generate_response(client, messages: List[Dict], model: str, temperature: float, max_tokens: int) -> Dict:
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
        response = chat_completion.choices[0].message.content if hasattr(chat_completion.choices[0], 'message') else chat_completion.choices[0].text
        return {"input": messages[-1]['content'], "output": response}
    except Exception as e:
        logging.error(f"Error generating response: {e}")
        raise

def extract_premise(affirmative_argument: str) -> str:
    premise_list = affirmative_argument.split(".")
    combined_premises_text = "\n".join(f"\"{premise.strip()}\"" for i, premise in enumerate(premise_list) if premise.strip())
    return combined_premises_text

def generate_counterargument(client, topic: str, affirmative_argument: str, prompts: Dict, model: str, temperature: float, max_tokens: int, condition: str) -> Dict:
    conversation_history = [
        {"role": "system", "content": prompts["system_prompt"]}
    ]
    steps = []

    try:
        premise_list = extract_premise(affirmative_argument)
        
        if condition == "x1":
            premise_prompt = prompts["x1"]["premise_generation_prompt"].replace("#topic#", topic).replace("#argument#", affirmative_argument)
            conversation_history.append({"role": "user", "content": premise_prompt})
            step_result = generate_response(client, conversation_history, model, temperature, max_tokens)
            steps.append({"step": "premise_generation", "input": premise_prompt, "output": step_result["output"]})
            conversation_history.append({"role": "assistant", "content": step_result["output"]})

            decision_prompt = prompts["x1"]["premise_decision_prompt"]
            conversation_history.append({"role": "user", "content": decision_prompt})
            step_result = generate_response(client, conversation_history, model, temperature, max_tokens)
            steps.append({"step": "premise_decision", "input": decision_prompt, "output": step_result["output"]})
            conversation_history.append({"role": "assistant", "content": step_result["output"]})

            counterargument_prompt = prompts["x1"]["counter-argument_generation_prompt"]
            conversation_history.append({"role": "user", "content": counterargument_prompt})

        elif condition in ["x2", "x3"]:
            decision_prompt = prompts[condition]["premise_decision_prompt"].replace("#topic#", topic).replace("#argument#", affirmative_argument).replace("###premise_list###", premise_list)
            conversation_history.append({"role": "user", "content": decision_prompt})
            step_result = generate_response(client, conversation_history, model, temperature, max_tokens)
            steps.append({"step": "premise_decision", "input": decision_prompt, "output": step_result["output"]})
            conversation_history.append({"role": "assistant", "content": step_result["output"]})

            counterargument_prompt = prompts[condition]["counter-argument_generation_prompt"]
            conversation_history.append({"role": "user", "content": counterargument_prompt})

        elif condition in ["x4", "x7"]:
            counterargument_prompt = prompts[condition]["counter-argument_generation_prompt"].replace("#topic#", topic).replace("#argument#", affirmative_argument)
            conversation_history.append({"role": "user", "content": counterargument_prompt})

        elif condition == ["x5","x6"]:
            counterargument_prompt = prompts[condition]["counter-argument_generation_prompt"].replace("#topic#", topic).replace("#argument#", affirmative_argument).replace("###premise_list###", premise_list)
            conversation_history.append({"role": "user", "content": counterargument_prompt})

        else:
            raise ValueError(f"Invalid condition: {condition}")

        step_result = generate_response(client, conversation_history, model, temperature, max_tokens)
        steps.append({"step": "counterargument_generation", "input": counterargument_prompt, "output": step_result["output"]})

        return {"counterargument": step_result["output"], "steps": steps}

    except Exception as e:
        logging.error(f"Error generating counterargument: {e}")
        raise