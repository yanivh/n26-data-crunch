# Test data for dimension deduplication
SAMPLE_DATA = [
    {'sk_agrmnt_id': 1, 'agrmnt_id': 101, 'actual_from_dt': '2015-01-01', 'actual_to_dt': '2015-02-20', 'client_id': 20, 'product_id': 305, 'interest_rate': 3.5},
    {'sk_agrmnt_id': 2, 'agrmnt_id': 101, 'actual_from_dt': '2015-02-21', 'actual_to_dt': '2015-05-17', 'client_id': 20, 'product_id': 345, 'interest_rate': 4.0},
    {'sk_agrmnt_id': 3, 'agrmnt_id': 101, 'actual_from_dt': '2015-05-18', 'actual_to_dt': '2015-07-05', 'client_id': 20, 'product_id': 345, 'interest_rate': 4.0},
    {'sk_agrmnt_id': 4, 'agrmnt_id': 101, 'actual_from_dt': '2015-07-06', 'actual_to_dt': '2015-08-22', 'client_id': 20, 'product_id': 539, 'interest_rate': 6.0},
    {'sk_agrmnt_id': 5, 'agrmnt_id': 101, 'actual_from_dt': '2015-08-23', 'actual_to_dt': '9999-12-31', 'client_id': 20, 'product_id': 345, 'interest_rate': 4.0},
    {'sk_agrmnt_id': 6, 'agrmnt_id': 102, 'actual_from_dt': '2016-01-01', 'actual_to_dt': '2016-06-30', 'client_id': 25, 'product_id': 333, 'interest_rate': 3.7},
    {'sk_agrmnt_id': 7, 'agrmnt_id': 102, 'actual_from_dt': '2016-07-01', 'actual_to_dt': '2016-07-25', 'client_id': 25, 'product_id': 333, 'interest_rate': 3.7},
    {'sk_agrmnt_id': 8, 'agrmnt_id': 102, 'actual_from_dt': '2016-07-26', 'actual_to_dt': '2016-09-15', 'client_id': 25, 'product_id': 333, 'interest_rate': 3.7},
    {'sk_agrmnt_id': 9, 'agrmnt_id': 102, 'actual_from_dt': '2016-09-16', 'actual_to_dt': '9999-12-31', 'client_id': 25, 'product_id': 560, 'interest_rate': 5.9},
    {'sk_agrmnt_id': 10, 'agrmnt_id': 103, 'actual_from_dt': '2011-05-22', 'actual_to_dt': '9999-12-31', 'client_id': 30, 'product_id': 560, 'interest_rate': 2.0}
]

# Column definitions
COLUMNS = [
    'sk_agrmnt_id',
    'agrmnt_id',
    'actual_from_dt',
    'actual_to_dt',
    'client_id',
    'product_id',
    'interest_rate'
] 