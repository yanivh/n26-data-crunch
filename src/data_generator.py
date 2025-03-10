# Copyright 2020 N26 GmbH

import csv
import os
import random
import uuid
from typing import Dict, List, Any
from utils import write_data
from collections import defaultdict
from datetime import datetime, timedelta


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

        # Fix the datetime usage here
        current_date = datetime.now().date() - timedelta(
            days=random.randint(int(i / len(active_transaction_users)), 100)
        )

        transaction = [
            uuid.uuid4(),
            current_date.strftime('%Y-%m-%d'),
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


def generate_agreements(users):
    """Generate agreement data for users."""
    header = [
        'sk_agrmnt_id',
        'agrmnt_id',
        'actual_from_dt',
        'actual_to_dt',
        'client_id',
        'product_id',
        'interest_rate'
    ]
    
    data = []
    sk_agrmnt_id = 1
    
    for user in users['data']:
        user_id = user[0]  # Assuming user_id is first column
        
        # Generate 1-3 agreements per user
        num_agreements = random.randint(1, 3)
        
        # Start date for first agreement
        current_date = datetime(2015, 1, 1) + timedelta(days=random.randint(0, 365))
        
        for _ in range(num_agreements):
            # Generate agreement duration (30-365 days)
            duration = timedelta(days=random.randint(30, 365))
            
            # End date is start date + duration
            end_date = current_date + duration
            
            # Generate random product_id (300-600)
            product_id = random.randint(300, 600)
            
            # Generate random interest rate (1.0-10.0)
            interest_rate = round(random.uniform(1.0, 10.0), 2)
            
            data.append([
                sk_agrmnt_id,
                f"AGR{sk_agrmnt_id:06d}",
                current_date.strftime('%Y-%m-%d'),
                end_date.strftime('%Y-%m-%d'),
                user_id,
                product_id,
                interest_rate
            ])
            
            sk_agrmnt_id += 1
            # Next agreement starts when current one ends
            current_date = end_date
    
    return {
        'header': header,
        'data': data
    } 