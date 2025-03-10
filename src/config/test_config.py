# Test configuration settings

import uuid

# Generate some sample UUIDs
USERS = [
    (str(uuid.uuid4()), True),  # active user
    (str(uuid.uuid4()), False), # inactive user
    (str(uuid.uuid4()), True)   # active user
]

# Test data for transactions
SAMPLE_DATA = [
    {'transaction_id': 'ef05-4247', 'user_id': 'becf-457e', 'date': '2020-01-01'},
    {'transaction_id': 'c8d1-40ca', 'user_id': 'becf-457e', 'date': '2020-01-05'},
    {'transaction_id': 'fc2b-4b36', 'user_id': 'becf-457e', 'date': '2020-01-07'},
    {'transaction_id': '3725-48c4', 'user_id': 'becf-457e', 'date': '2020-01-15'},
    {'transaction_id': '5f2a-47c2', 'user_id': 'becf-457e', 'date': '2020-01-16'},
    {'transaction_id': '7541-412c', 'user_id': '5728-4f1c', 'date': '2020-01-01'},
    {'transaction_id': '3deb-47d7', 'user_id': '5728-4f1c', 'date': '2020-01-12'}
]

# Column definitions
TRANSACTION_COLUMNS = [
    'transaction_id',
    'date',
    'user_id',
    'is_blocked',
    'transaction_amount',
    'transaction_category_id'
]

USER_COLUMNS = [
    'user_id',
    'is_active'
]

# Query file paths
MAIN_QUERY_PATH = 'src/queries/feature_table/main.sql'
ALTERNATIVE_QUERY_PATH = 'src/queries/feature_table/alternative_solutions.sql'

# Expected columns in the feature table
EXPECTED_COLUMNS = [
    'transaction_id',
    'user_id',
    'date',
    '# Transactions within previous 7 days'
] 