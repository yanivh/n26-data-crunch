import csv
import os
from datetime import datetime
from join_datasets import process_transactions, load_users, load_agreements
import main  # Import main instead of data_generator

def run_tests():
    """Run the join datasets tests."""
    try:
        # Define file paths
        users_path = 'data/users.csv'
        transactions_path = 'data/transactions.csv'
        agreements_path = 'data/dim_dep_agreement.csv'  # Add this path

        # Load test data
        users_dict = load_users(users_path)
        agreements_dict = load_agreements(agreements_path)  # Use the path
        
        # Process transactions
        results = process_transactions(transactions_path, users_dict, agreements_dict)
        
        # Validate results
        validate_results(results)
        
        print("All tests passed successfully!")
        return True
        
    except Exception as e:
        print(f"Test failed: {e}")
        return False

def validate_results(results):
    # Read original transactions to compare
    transactions = []
    with open('data/transactions.csv', 'r') as f:
        reader = csv.DictReader(f)
        transactions = list(reader)
    
    # Basic validation
    assert len(results) == len(transactions), f"Expected {len(transactions)} results, got {len(results)}"
    
    # Verify each transaction has required fields
    for result in results:
        assert 'transaction_id' in result, "Missing transaction_id"
        assert 'user_id' in result, "Missing user_id"
        assert 'transaction_date' in result, "Missing transaction_date"
        assert 'is_blocked' in result, "Missing is_blocked"
        assert 'is_active' in result, "Missing is_active"
        # product_id and interest_rate may be None for transactions without matching agreements

    print("\nResults summary:")
    print(f"Total transactions processed: {len(results)}")
    print(f"Transactions with agreements: {len([r for r in results if r['product_id'] is not None])}")
    print(f"Active users: {len([r for r in results if r['is_active']])}")
    print(f"Blocked transactions: {len([r for r in results if r['is_blocked']])}")

if __name__ == "__main__":
    print("Starting join datasets test...")
    run_tests()
    print("Tests completed successfully.") 