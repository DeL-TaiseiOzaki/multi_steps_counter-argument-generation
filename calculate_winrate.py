import json
from collections import defaultdict

def calculate_detailed_win_rates(data_list):
    """
    Calculate win rates for x1 by model and evaluation criteria
    
    Args:
        data_list (list): List of dictionaries containing evaluation results
        
    Returns:
        tuple: (model_win_rates, overall_criterion_rates, total_win_rate)
    """
    # Initialize counters
    wins = defaultdict(lambda: defaultdict(int))
    totals = defaultdict(lambda: defaultdict(int))
    
    # For overall statistics by criterion
    overall_wins = defaultdict(int)
    overall_totals = defaultdict(int)
    
    # For total statistics
    total_wins = 0
    total_evaluations = 0
    
    # Process each record
    for data in data_list:
        evaluation_results = data.get('evaluation_results', {})
        
        # For each model
        for model in ['mini', 'gpt', 'llama']:
            if model not in evaluation_results:
                continue
                
            evaluations = evaluation_results[model]
            
            # Process each evaluation criterion
            for eval_item in evaluations:
                criterion_name = eval_item['name']
                try:
                    result = json.loads(eval_item['result'])
                    
                    # Count total evaluations
                    totals[model][criterion_name] += 1
                    overall_totals[criterion_name] += 1
                    total_evaluations += 1
                    
                    # Count wins for x1
                    if result[0] == 1:  # 1 represents x1
                        wins[model][criterion_name] += 1
                        overall_wins[criterion_name] += 1
                        total_wins += 1
                        
                except json.JSONDecodeError:
                    print(f"Skipping invalid result format for {model} - {criterion_name}")
                    continue
    
    # Calculate win rates by model and criterion
    win_rates = {}
    for model in wins.keys():
        win_rates[model] = {}
        for criterion in wins[model].keys():
            if totals[model][criterion] > 0:
                win_rate = (wins[model][criterion] / totals[model][criterion]) * 100
                win_rates[model][criterion] = win_rate
    
    # Calculate overall win rates by criterion
    overall_criterion_rates = {}
    for criterion in overall_totals.keys():
        if overall_totals[criterion] > 0:
            win_rate = (overall_wins[criterion] / overall_totals[criterion]) * 100
            overall_criterion_rates[criterion] = win_rate
    
    # Calculate total win rate
    total_win_rate = (total_wins / total_evaluations * 100) if total_evaluations > 0 else 0
    
    return win_rates, overall_criterion_rates, total_win_rate

def process_json_file(file_path):
    """
    Process a JSON file and calculate detailed win rates
    
    Args:
        file_path (str): Path to the JSON file
        
    Returns:
        tuple: (model_win_rates, overall_criterion_rates, total_win_rate)
    """
    try:
        # Read JSON file
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Ensure data is a list
        if isinstance(data, dict):
            data = [data]
            
        return calculate_detailed_win_rates(data)
            
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {file_path}")
        return None
    except Exception as e:
        print(f"Error processing file: {e}")
        return None

def display_win_rates(model_win_rates, overall_criterion_rates, total_win_rate):
    """
    Display win rates in a formatted way
    """
    if not model_win_rates:
        return
        
    print("\nDetailed Win Rates for X1:")
    print("=" * 80)
    
    # Display per model statistics
    for model in model_win_rates.keys():
        print(f"\nModel: {model.upper()}")
        print("-" * 40)
        
        for criterion, rate in model_win_rates[model].items():
            print(f"{criterion:<50}: {rate:>6.2f}%")
    
    # Display overall statistics by criterion
    print("\nOVERALL STATISTICS BY CRITERION")
    print("-" * 40)
    for criterion, rate in overall_criterion_rates.items():
        print(f"{criterion:<50}: {rate:>6.2f}%")
    
    # Display total win rate
    print("\nTOTAL WIN RATE")
    print("-" * 40)
    print(f"Overall win rate across all models and criteria: {total_win_rate:>6.2f}%")

# Example usage
if __name__ == "__main__":
    file_path = "evaluation_results_3v6.json"  # JSONファイルのパスを指定
    results = process_json_file(file_path)
    
    if results:
        model_win_rates, overall_criterion_rates, total_win_rate = results
        display_win_rates(model_win_rates, overall_criterion_rates, total_win_rate)