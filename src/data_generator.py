# Copyright 2020 N26 GmbH

import csv
import datetime
import os
import random
import uuid
from typing import Dict, List, Any
from utils import write_data
from collections import defaultdict


def generate_transactions(users: Dict[str, Any]) -> Dict[str, Any]:
    """Generate random transaction data."""
    num_transactions = 10000
    num_users = len(users['data'])

    header = [
        'transaction_id',
        'date',
        'user_id',
        'is_blocked',
        'transaction_amount',
        'transaction_category_id'
    ]

    # Each user will have 1 preferred category (even more realistic)
    user_preferences = {
        str(users['data'][i][0]): set(
            random.sample(range(11), random.randint(1, 1))  # Each user uses 1 categoy
        ) for i in range(num_users)
    }

    # Track how many users per category for validation
    category_users = defaultdict(set)
    
    # Select a subset of users who will have transactions
    active_transaction_users = random.sample(
        [str(user[0]) for user in users['data']], 
        k=min(1000, num_users)  #  1000 users will have transactions
    )

    data = []
    # Distribute transactions among active users
    for i in range(num_transactions):
        user_id = random.choice(active_transaction_users)
        preferred_categories = user_preferences[user_id]
        
        # 95% chance to use preferred category, 5% chance for random
        category_id = (
            random.choice(list(preferred_categories))
            if random.random() < 0.95  # Higher preference for user's categories
            else random.randint(0, 10)
        )

        transaction = [
            uuid.uuid4(),
            (datetime.date.today() - datetime.timedelta(
                days=random.randint(int(i / len(active_transaction_users)), 100)
            )).strftime('%Y-%m-%d'),
            user_id,
            'True' if random.random() < 0.01 else 'False',
            '%.2f' % (random.random() * 50),
            category_id
        ]
        data.append(transaction)
        
        # Track category usage
        category_users[category_id].add(user_id)

    # Print validation info
    print("\nData Generation Statistics:")
    print(f"Total users in database: {num_users}")
    print(f"Users with transactions: {len(active_transaction_users)}")
    print("\nUsers per category:")
    for category in range(11):
        print(f"Category {category}: {len(category_users[category])} unique users")
    
    # Validate distribution
    total_preferences = sum(len(prefs) for prefs in user_preferences.values())
    avg_categories_per_user = total_preferences / len(user_preferences)
    print(f"\nAverage categories per user: {avg_categories_per_user:.2f}")

    return {'header': header, 'data': data}


def generate_users() -> Dict[str, Any]:
    """Generate random user data."""
    num_users = 1000
    header = [
        'user_id',
        'is_active'
    ]

    data = [[
        uuid.uuid4(),
        '1' if random.random() < 0.9 else '0'
    ] for _ in range(num_users)]

    return {'header': header, 'data': data}


def write_data(out: str, header: List[str], data: List[List[Any]]) -> bool:
    """Write data to CSV file."""
    if os.path.exists(out):
        print('File %s already exists!' % out)
        return False

    try:
        with open(out, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(data)
    except Exception as err:
        print('Failed to write %s' % out)
        return False
    return True 