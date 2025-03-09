import csv
from collections import defaultdict
from typing import Dict, Set, Tuple, List
from user_service import read_active_users


def process_transactions(filename: str, active_users: Set[str]) -> Dict[int, Tuple[int, Set[str]]]:
    """
    Process transactions and return aggregated data by category.
    Returns dict with category_id -> (sum_amount, set of unique user_ids)
    """
    category_data = defaultdict(lambda: (0, set()))  # (sum_amount, set of unique users)
    
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Skip if transaction is blocked or user not active
            if row['is_blocked'] == 'True' or row['user_id'] not in active_users:
                continue
                
            category_id = int(row['transaction_category_id'])
            amount = int(float(row['transaction_amount']))
            user_id = row['user_id']
            
            # Update category data
            current_sum, current_users = category_data[category_id]
            # Add this user to the set of users for this category
            current_users.add(user_id)  # Using set ensures uniqueness
            category_data[category_id] = (current_sum + amount, current_users)
    
    return category_data


def format_results(category_data: Dict[int, Tuple[int, Set[str]]]) -> List[Tuple[int, int, int]]:
    """
    Format and sort the results.
    Returns list of (category_id, sum_amount, number_of_unique_users)
    """
    results = [
        (category_id, sum_amount, len(users))  # len(users) gives count of unique users
        for category_id, (sum_amount, users) in category_data.items()
    ]
    results.sort(key=lambda x: x[1], reverse=True)  # Sort by sum_amount descending
    return results 