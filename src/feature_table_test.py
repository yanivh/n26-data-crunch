import duckdb
import pandas as pd
from datetime import datetime, timedelta
from config.test_config import SAMPLE_DATA, EXPECTED_COLUMNS
import sys

def read_query_file(file_path):
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading query file: {e}")
        return None

def run_tests():
    try:
        print("Initializing DuckDB...")
        # Initialize DuckDB with more memory and debug logging
        conn = duckdb.connect(':memory:', config={'memory_limit': '2GB'})
        
        print("Creating test data...")
        # Create DataFrame
        df = pd.DataFrame(SAMPLE_DATA)
        
        print("\nOriginal Transaction Data:")
        print(df[['transaction_id', 'user_id', 'date']].sort_values(['user_id', 'date']).to_string(index=False))
        
        print("\nCreating transactions table...")
        # Register DataFrame as a table
        conn.register('transactions', df)
        
        print("\nVerifying table creation...")
        result = conn.execute("SELECT COUNT(*) FROM transactions").fetchone()
        print(f"Number of rows in transactions table: {result[0]}")

        print("\nCalculating 7-day window counts...")
        # Read and execute SQL query
        with open('src/queries/feature_table/main.sql', 'r') as f:
            query = f.read()
        
        # Execute query
        result = conn.execute(query).fetchdf()
        
        # Verify columns
        assert all(col in result.columns for col in EXPECTED_COLUMNS), "Missing expected columns"
        
        print("\nFeature Table Results:")
        print("transaction_id | user_id     | date       | # Transactions within previous 7 days")
        print("-" * 75)
        for _, row in result.sort_values(['user_id', 'date']).iterrows():
            print(f"{row['transaction_id']:<13} | {row['user_id']:<11} | {row['date']} | {row['# Transactions within previous 7 days']:>3}")

        # Print explanation for a few examples
        print("\nExample Explanations:")
        print("1. For user becf-457e on 2020-01-05:")
        print("   - Looking back 7 days (2019-12-29 to 2020-01-04)")
        print("   - Found 1 transaction (2020-01-01)")
        
        print("\n2. For user becf-457e on 2020-01-07:")
        print("   - Looking back 7 days (2019-12-31 to 2020-01-06)")
        print("   - Found 2 transactions (2020-01-01 and 2020-01-05)")

        # Add validation for specific test cases
        expected_results = {
            ('ef05-4247', 'becf-457e', '2020-01-01'): 0,  # First transaction
            ('c8d1-40ca', 'becf-457e', '2020-01-05'): 1,  # One transaction in last 7 days
            ('fc2b-4b36', 'becf-457e', '2020-01-07'): 2,  # Two transactions in last 7 days
            ('3725-48c4', 'becf-457e', '2020-01-15'): 0,  # No transactions in last 7 days
            ('5f2a-47c2', 'becf-457e', '2020-01-16'): 1   # One transaction in last 7 days
        }

        for idx, row in result.iterrows():
            key = (row['transaction_id'], row['user_id'], row['date'])
            if key in expected_results:
                assert row['transactions_last_7_days'] == expected_results[key], \
                    f"Mismatch for {key}: expected {expected_results[key]}, got {row['transactions_last_7_days']}"

        print("\nClosing connection...")
        conn.close()

    except Exception as e:
        print(f"Error during test execution: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    print("Starting feature table tests...")
    run_tests()
    print("Tests completed successfully.") 