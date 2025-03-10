import duckdb
import pandas as pd
from config.dimension_test_config import SAMPLE_DATA, COLUMNS
import sys
from datetime import datetime

def read_query_file(file_path):
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading query file: {e}")
        return None

def run_tests():
    try:
        print("Starting dimension deduplication tests...")
        print("Initializing DuckDB...")
        conn = duckdb.connect(':memory:')
        
        print("Creating test data...")
        # Create DataFrame with proper date types
        df = pd.DataFrame(SAMPLE_DATA, columns=COLUMNS)
        
        print("\nOriginal Dimension Data:")
        print(df.to_string(index=False))
        
        print("\nCreating dimension table...")
        conn.register('dim_dep_agreement', df)
        
        print("\nDeduplicating records...")
        # Read and execute SQL query
        with open('src/queries/dimension_deduplication/dimension_deduplication_optimized.sql', 'r') as f:
            query = f.read()
        
        result = conn.execute(query).fetchdf()
        
        # Print statistics and analysis
        print("\nDeduplication Analysis:")
        print("-" * 50)
        print(f"Original records: {len(df)}")
        print(f"Deduplicated records: {len(result)}")
        print(f"Removed duplicates: {len(df) - len(result)}")
        
        # Analyze changes by agreement
        for agrmnt_id in sorted(df['agrmnt_id'].unique()):
            print(f"\nAgreement {agrmnt_id}:")
            orig = df[df['agrmnt_id'] == agrmnt_id]
            dedup = result[result['agrmnt_id'] == agrmnt_id]
            
            if len(orig) > len(dedup):
                print(f"  Removed {len(orig) - len(dedup)} duplicate records:")
                # Group consecutive records with same values
                current_group = []
                for idx, row in orig.iterrows():
                    if not current_group:
                        current_group.append(row)
                    else:
                        prev = current_group[-1]
                        if (prev['product_id'] == row['product_id'] and 
                            prev['interest_rate'] == row['interest_rate']):
                            current_group.append(row)
                        else:
                            if len(current_group) > 1:
                                print(f"    - Merged {len(current_group)} records from {current_group[0]['actual_from_dt']} "
                                      f"to {current_group[-1]['actual_to_dt']}")
                                print(f"      Product: {current_group[0]['product_id']}, "
                                      f"Rate: {current_group[0]['interest_rate']}%")
                            current_group = [row]
                
                # Handle last group
                if len(current_group) > 1:
                    print(f"    - Merged {len(current_group)} records from {current_group[0]['actual_from_dt']} "
                          f"to {current_group[-1]['actual_to_dt']}")
                    print(f"      Product: {current_group[0]['product_id']}, "
                          f"Rate: {current_group[0]['interest_rate']}%")
            else:
                print("  No duplicates found")
        
        print("\nDeduplicated Results:")
        print(result.to_string(index=False))
        
        conn.close()
        
    except Exception as e:
        print(f"Error during test execution: {e}")
        raise

if __name__ == "__main__":
    run_tests()
    print("Tests completed successfully.") 