import duckdb
import pandas as pd
from config.dimension_test_config import SAMPLE_DATA, COLUMNS
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
        conn = duckdb.connect(':memory:', config={'memory_limit': '2GB'})
        
        print("Creating test data...")
        df = pd.DataFrame(SAMPLE_DATA, columns=COLUMNS)
        
        print("\nOriginal Dimension Data:")
        print(df.to_string(index=False))
        
        print("\nCreating dimension table...")
        conn.execute("""
            CREATE TABLE dim_dep_agreement AS 
            SELECT 
                sk_agrmnt_id,
                agrmnt_id,
                CAST(actual_from_dt AS DATE) as actual_from_dt,
                CASE 
                    WHEN actual_to_dt = '9999-12-31' THEN NULL
                    ELSE CAST(actual_to_dt AS DATE)
                END as actual_to_dt,
                client_id,
                product_id,
                CAST(interest_rate AS DECIMAL(5,2)) as interest_rate
            FROM df
        """)

        print("\nDeduplicating records...")
        dedup_query = read_query_file('src/queries/dimension_deduplication/dimension_deduplication.sql')
        optimized_query = read_query_file('src/queries/dimension_deduplication/dimension_deduplication_optimized.sql')

        # Run both queries and compare results
        result = conn.execute(dedup_query).fetchdf()
        result_optimized = conn.execute(optimized_query).fetchdf()

        print("\nResults match:", result.equals(result_optimized))

        # Print statistics
        print("\nDeduplication Statistics:")
        print(f"Original records: {len(df)}")
        print(f"Deduplicated records: {len(result)}")
        print(f"Removed duplicates: {len(df) - len(result)}")

        # Print explanation of changes
        print("\nChanges Explained:")
        for agrmnt_id in sorted(df['agrmnt_id'].unique()):
            orig = df[df['agrmnt_id'] == agrmnt_id]
            dedup = result[result['agrmnt_id'] == agrmnt_id]
            print(f"\nAgreement {agrmnt_id}:")
            print(f"  Original records: {len(orig)}")
            print(f"  After deduplication: {len(dedup)}")
            if len(orig) > len(dedup):
                print(f"  Removed {len(orig) - len(dedup)} duplicate records")
                print("  Changes:")
                for _, row in dedup.iterrows():
                    print(f"    {row['actual_from_dt']} to {row['actual_to_dt']}: "
                          f"Product {row['product_id']}, Rate {row['interest_rate']}%")

        print("\nClosing connection...")
        conn.close()

    except Exception as e:
        print(f"Error during test execution: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    print("Starting dimension deduplication tests...")
    run_tests()
    print("Tests completed successfully.") 