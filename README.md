# N26 Data Engineering Challenge 2025

## Overview
This repository contains my solution to the N26 Data Engineering Challenge. The challenge consists of three main tasks that test different aspects of data engineering skills: data processing, feature computation, and dimension deduplication.

**Initial Implementation:**
- Created modular Python code structure.
- devlope a Initial SQL query for the feature table and dimension deduplication.
- Implemented processing logic.
- Focused on maintainability and single responsibility principle.
- Write README.md file.

**Improvements:**
- Enhanced data generation for more realistic distributions.
- Improved code organization and documentation.
- Optimized Queries and memory usage and performance.
- Create Makefile and docker files for easy setup and execution.
- Create Test files for each task.
- Enhanced  README.md file.


```bash
# First, build the Docker image (required once)
make docker-build

# Then run tests for each task:

# Task 1: Join Datasets
make docker-join-test

# Task 2: Feature Table
make docker-feature-table

# Task 3: Dimension Deduplication
make docker-dimension-test
```

## Approach & Methodology
I approached this challenge with a combination of hands-on experience and modern engineering practices. While I initially developed solutions based on my expertise, I also leveraged AI tools (specifically LLM) to validate and enhance my approaches. This reflects my belief that effective engineering involves using all available tools wisely while maintaining critical thinking and code quality.

## Tools & Technologies
- Python for data processing
- SQL for data analysis
- Git for version control
- Cursor AI for LLM support
- Docker for containerized execution
- Makefile for easy setup and execution
- DuckDB for database operations


## Task Breakdown

### Task 1: Joining Data Sets
**Description:**
Joins multiple datasets (transactions, users, and agreements) efficiently while maintaining data integrity.

Reviewing this task, I pay special attention not only to the correctness of results, but especially to the code quality and efficiency of the data structures and algorithms used. The implementation uses hash tables for O(1) lookups and minimizes memory usage through generator patterns where applicable.

**Run the tests:**
```bash
# Build Docker image (required once)
make docker-build

# Run join datasets tests
make docker-join-test
```

### Task 2: Feature Table Computation
**Challenge:**
Computing a feature table for transactions, calculating the number of transactions within the previous seven days for each user.

Under the hood, when executing this query, the database engine performs several optimization steps:
1. Query Planning: Creates execution plan using statistics about data distribution
2. Index Usage: Leverages temporal indexes for efficient date-range filtering
3. Window Functions: Optimizes sliding window calculations using partitioning
4. Memory Management: Uses hash aggregation for grouping when memory permits

**Run the tests:**
```bash
# Build Docker image (if not already built)
make docker-build

# Run feature table tests
make docker-feature-table
```

### Task 3: Dimension Deduplication
**Challenge:**
Optimize storage and query performance by removing redundant records while maintaining data integrity.

**Script Logic:**
The deduplication process follows these key steps:
1. Identifies duplicate records using a combination of business keys
2. Maintains version history through effective dating
3. Implements soft deletes to preserve historical data
4. Uses window functions to determine the latest valid record
5. Optimizes storage by removing redundant data while maintaining referential integrity
6. Implements change tracking through SCD Type 2 methodology

**Run the tests:**
```bash
# Build Docker image (if not already built)
make docker-build

# Run dimension deduplication tests
make docker-dimension-test
```


## Prerequisites

- Python 3.9-3.11
- Docker (optional, for containerized execution)
  - [Install Docker Desktop](https://www.docker.com/products/docker-desktop/)
  - Or using Homebrew: `brew install --cask docker`
- Make (optional, for using Makefile commands)

## Project Structure

```
.
├── src/
│   ├── data_generator.py  # Data generation logic
│   ├── data_processor.py  # Data processing utilities
│   ├── join_datasets.py   # Dataset joining implementation
│   ├── main.py           # Main entry point
│   └── queries/          # SQL queries

```

## Quick Start

1. Clone the repository:
```bash
git clone <git@github.com:yanivh/n26-data-crunch.git>
cd <n26-data-crunch>
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


## Makefile Commands

- `make docker-build`: Build Docker image
- `make docker-join-test`: Run tests in Docker
- `make docker-join-run`: Run main program in Docker
- `make setup`: Set up local Python environment
- `make join-test`: Run tests locally
- `make generate`: Generate test data
- `make clean`: Clean generated files



## License

[n26-data-crunch@yanivh]





