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





