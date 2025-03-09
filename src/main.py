from data_generator import generate_users, generate_transactions
from data_processor import process_transactions, format_results
from user_service import read_active_users
from utils import write_data


def generate_data_files():
    """Generate and write data files."""
    print("Generating data files...")
    users = generate_users()
    transactions = generate_transactions(users)

    print(f"Generated {len(users['data'])} users")
    print(f"Generated {len(transactions['data'])} transactions")

    write_data('users.csv', users['header'], users['data'])
    write_data('transactions.csv', transactions['header'], transactions['data'])


def process_data():
    """Process the data files and return results."""
    print("\nProcessing data...")
    active_users = read_active_users('users.csv')
    print(f"Found {len(active_users)} active users")
    
    category_data = process_transactions('transactions.csv', active_users)
    print(f"Found {len(category_data)} transaction categories")
    
    results = format_results(category_data)
    print(f"Generated {len(results)} result rows")
    return results


def print_results(results):
    """Print results in CSV format."""
    print("\nResults:")
    print("transaction_category_id,sum_amount,num_users")
    if not results:
        print("No results found!")
        return
        
    for category_id, sum_amount, num_users in results:
        print(f"{category_id},{sum_amount},{num_users}")


def main():
    # Generate data files
    generate_data_files()
    
    # Process data and get results
    results = process_data()
    
    # Print results
    print_results(results)


if __name__ == '__main__':
    main() 