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
    (str(uuid.uuid4()), '2020-01-01', USERS[0][0], False, 100, 1),
    (str(uuid.uuid4()), '2020-01-05', USERS[0][0], False, 200, 2),
    (str(uuid.uuid4()), '2020-01-07', USERS[0][0], True,  150, 1),
    (str(uuid.uuid4()), '2020-01-15', USERS[1][0], False, 300, 3),
    (str(uuid.uuid4()), '2020-01-16', USERS[2][0], False, 250, 2)
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