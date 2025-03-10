import csv
from collections import defaultdict
from datetime import datetime
import sys
from typing import Dict, List, Set, Tuple
import os

def parse_date(date_str: str) -> datetime:
    """Parse date string to datetime object."""
    return datetime.strptime(date_str, '%Y-%m-%d')

def load_users(filename: str) -> Dict[str, bool]:
    """Load users and their active status into memory."""
    users = {}
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            users[row['user_id']] = row['is_active'].lower() == 'true'
    return users

def load_agreements(filename: str) -> Dict[str, List[Tuple[datetime, datetime, int, float]]]:
    """Load agreements into memory, organized by client_id."""
    agreements = defaultdict(list)
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            client_id = row['client_id']
            from_date = parse_date(row['actual_from_dt'])
            to_date = parse_date(row['actual_to_dt'])
            product_id = int(row['product_id'])
            interest_rate = float(row['interest_rate'])
            agreements[client_id].append((from_date, to_date, product_id, interest_rate))
    return agreements

def find_matching_agreement(
    agreements: List[Tuple[datetime, datetime, int, float]], 
    transaction_date: datetime
) -> Tuple[int, float]:
    """Find matching agreement for transaction date."""
    for from_date, to_date, product_id, interest_rate in agreements:
        if from_date <= transaction_date < to_date:
            return product_id, interest_rate
    return None, None

def process_transactions(
    trans_file: str,
    users: Dict[str, bool],
    agreements: Dict[str, List[Tuple[datetime, datetime, int, float]]]
) -> List[dict]:
    """Process transactions and join with user and agreement data."""
    results = []
    
    with open(trans_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            transaction_date = parse_date(row['date'])
            user_id = row['user_id']
            
            # Get user status
            is_active = users.get(user_id, False)
            
            # Find matching agreement
            user_agreements = agreements.get(user_id, [])
            product_id, interest_rate = find_matching_agreement(user_agreements, transaction_date)
            
            results.append({
                'transaction_id': row['transaction_id'],
                'transaction_date': row['date'],
                'user_id': user_id,
                'is_blocked': row['is_blocked'].lower() == 'true',
                'transaction_amount': int(row['transaction_amount']),
                'transaction_category_id': int(row['transaction_category_id']),
                'is_active': is_active,
                'product_id': product_id,
                'interest_rate': interest_rate
            })
    
    return sorted(results, key=lambda x: (x['transaction_date'], x['transaction_id']))

def print_results(results: List[dict]) -> None:
    """Print results in CSV format."""
    if not results:
        return
    
    headers = results[0].keys()
    writer = csv.DictWriter(sys.stdout, fieldnames=headers)
    writer.writeheader()
    writer.writerows(results)

def main():
    """Main function to process and join datasets."""
    try:
        # Look in the mounted directory
        users = load_users('/app/data/user_data.csv')
        agreements = load_agreements('/app/data/dim_dep_agreement.csv')
        results = process_transactions('/app/data/transaction_data.csv', users, agreements)
        print_results(results)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please ensure data files are generated using 'make generate' first")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 