import duckdb
import pandas as pd
from datetime import datetime
from config.test_config import SAMPLE_DATA, COLUMNS
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
        df = pd.DataFrame(SAMPLE_DATA, columns=COLUMNS)
        
        print("\nOriginal Transaction Data:")
        print(df.sort_values(['user_id', 'date']).to_string(index=False))
        
        print("\nCreating transactions table...")
        # Create table in DuckDB
        conn.execute("""
            CREATE TABLE transactions AS 
            SELECT 
                transaction_id,
                user_id,
                CAST(date AS DATE) as date
            FROM df
        """)
        
        print("\nVerifying table creation...")
        result = conn.execute("SELECT COUNT(*) FROM transactions").fetchone()
        print(f"Number of rows in transactions table: {result[0]}")

        print("\nCalculating 7-day window counts...")
        main_query = """
        WITH daily_counts AS (
            SELECT 
                transaction_id,
                user_id,
                date,
                CAST(
                    COALESCE(
                        COUNT(*) OVER (
                            PARTITION BY user_id 
                            ORDER BY date 
                            RANGE BETWEEN INTERVAL '7 days' PRECEDING AND INTERVAL '1 day' PRECEDING
                        ),
                        0
                    ) AS INTEGER
                ) as transactions_last_7_days
            FROM transactions
        )
        SELECT 
            transaction_id,
            user_id,
            date,
            transactions_last_7_days as "# Transactions within previous 7 days"
        FROM daily_counts
        ORDER BY user_id, date;
        """

        result = conn.execute(main_query).fetchdf()
        print("\nFeature Table Results (with 7-day window counts):")
        print(result.to_string(index=False))

        # Print explanation for a few examples
        print("\nExample Explanations:")
        print("1. For user becf-457e on 2020-01-05:")
        print("   - Looking back 7 days (2019-12-29 to 2020-01-04)")
        print("   - Found 1 transaction (2020-01-01)")
        
        print("\n2. For user becf-457e on 2020-01-07:")
        print("   - Looking back 7 days (2019-12-31 to 2020-01-06)")
        print("   - Found 2 transactions (2020-01-01 and 2020-01-05)")

        print("\nClosing connection...")
        conn.close()

    except Exception as e:
        print(f"Error during test execution: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    print("Starting feature table tests...")
    run_tests()
    print("Tests completed successfully.") 