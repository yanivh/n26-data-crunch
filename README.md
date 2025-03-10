# N26 Data Engineering Challenge 2025

## Overview
This repository contains my solution to the N26 Data Engineering Challenge. The challenge consists of three main tasks that test different aspects of data engineering skills: data processing, feature computation, and dimension deduplication.

## Approach & Methodology
I approached this challenge with a combination of hands-on experience and modern engineering practices. While I initially developed solutions based on my expertise, I also leveraged AI tools (specifically LLM) to validate and enhance my approaches. This reflects my belief that effective engineering involves using all available tools wisely while maintaining critical thinking and code quality.

## Tools & Technologies
- Python for data processing
- SQL for data analysis
- Git for version control
- Cursor AI for LLM support

## Task Breakdown

### Task 1: Joining Data Sets
**Initial Implementation:**
- Created modular Python code structure.
- Implemented processing logic.
- Focused on maintainability and single responsibility principle.

**Improvements:**
- Enhanced data generation for more realistic distributions.
- Improved code organization and documentation
- Optimized memory usage and performance
- Create Makefile and docker files for easy setup and execution.

**Run the solution:**
```bash
make all  # Generates and processes the data sets
```

### Task 2: Feature Table Computation
**Challenge:**
Computing a feature table for transactions, calculating the number of transactions within the previous seven days for each user.

**Solution Approach:**
- Implemented using Window Functions for efficient processing.
- Carefully considered performance implications.
- Added support for large dataset handling.

**Key Implementation Details:**
```sql
WITH daily_counts AS (
    SELECT 
        transaction_id,
        user_id,
        date,
        COUNT(*) OVER (
            PARTITION BY user_id 
            ORDER BY date 
            RANGE BETWEEN INTERVAL '7 days' PRECEDING AND 
            INTERVAL '1 day' PRECEDING
        ) as transactions_last_7_days
    FROM transactions
)
```

**Technical Highlights:**
- Efficient data partitioning by user
- Smart window frame management
- Parallel processing capabilities
- O(N log N) complexity for optimal performance

### Task 3: Dimension Deduplication
**Challenge:**
Optimize storage and query performance by removing redundant records while maintaining data integrity.

**Solution Evolution:**
1. Initial Approach (`dimension_deduplication.sql`):
   - Used window functions for change detection
   - Implemented basic deduplication logic

2. Optimized Solution (`dimension_deduplication_optimized.sql`):
   - Single-pass processing
   - Minimal memory footprint
   - More efficient window function usage

**Key Considerations:**
- Single table scan for performance
- Minimal memory usage
- Efficient use of window functions
- Maintaining data integrity

# Data Processing Pipeline

This project implements a data processing pipeline that generates test data, processes transactions, and joins datasets efficiently using Python's standard library.

## Prerequisites

- Python 3.9-3.11
- Docker (optional, for containerized execution)
  - [Install Docker Desktop](https://www.docker.com/products/docker-desktop/)
  - Or using Homebrew: `brew install --cask docker`
- Make (optional, for using Makefile commands)

## Project Structure

```
.
├── data/                  # Generated data files directory
├── src/
│   ├── data_generator.py  # Data generation logic
│   ├── data_processor.py  # Data processing utilities
│   ├── join_datasets.py   # Dataset joining implementation
│   ├── main.py           # Main entry point
│   └── queries/          # SQL queries
└── tests/                # Test files
```

## Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Choose your preferred execution method:

### Using Docker (Recommended)

```bash
# Build the Docker image
make docker-build

# Run the complete test suite
make docker-join-test

# Run the main program
make docker-join-run
```

### Using Local Python Environment

```bash
# Create virtual environment and install dependencies
make setup

# Run the test suite
make join-test

# Generate data and run main program
make generate
python src/join_datasets.py
```

## Step-by-Step Testing

### 1. Data Generation
Test the data generation process:
```bash
# Using Docker
make docker-build
docker run --rm -v $(PWD):/app/data n26-task:latest src/main.py

# Using local Python
make setup
make generate
```

Expected output: Statistics about generated users, transactions, and categories.

### 2. Data Processing
Test the data processing functionality:
```bash
# Using Docker
make docker-join-test

# Using local Python
make join-test
```

Expected output: Test results showing data validation and processing statistics.

### 3. Dataset Joining
Test the dataset joining implementation:
```bash
# Using Docker
make docker-join-run

# Using local Python
python src/join_datasets.py
```

Expected output: CSV format data showing joined transactions with user and agreement information.

## File Descriptions

- `main.py`: Entry point that generates test data
- `data_generator.py`: Contains logic for generating test data
- `data_processor.py`: Utilities for processing data
- `join_datasets.py`: Implements efficient dataset joining
- `join_datasets_test.py`: Tests for the joining implementation

## Data Files

The program generates and processes these files:
- `transaction_data.csv`: Transaction records
- `user_data.csv`: User information
- `dim_dep_agreement.csv`: Agreement dimension data

## Testing Strategy

1. **Unit Tests**: Individual component testing
2. **Integration Tests**: Testing data flow between components
3. **End-to-End Tests**: Complete pipeline testing

## Makefile Commands

- `make docker-build`: Build Docker image
- `make docker-join-test`: Run tests in Docker
- `make docker-join-run`: Run main program in Docker
- `make setup`: Set up local Python environment
- `make join-test`: Run tests locally
- `make generate`: Generate test data
- `make clean`: Clean generated files

## Error Handling

The program includes comprehensive error handling for:
- Missing data files
- Invalid data formats
- Processing errors

## Performance Considerations

- Uses efficient data structures for lookups
- Processes data in memory for better performance
- Implements sorting for consistent output

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Add your license information here]





