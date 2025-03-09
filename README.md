# n26-data-crunch


I approached the challenge by first breaking down the problem and outlining a solution. I implemented an initial version based on my experience, but to optimize my approach, I used an LLM to explore alternative solutions and validate my reasoning. While it provided useful insights, I carefully reviewed, modified, and tested the final solution to ensure it met best practices. In real-world development, leveraging tools efficiently is part of being an effective engineer, and I see AI as an enhancement rather than a replacement for critical thinking.

i write the steps i toke to solve the problem and the LLM parts that i used to validate my solution and improve it.

Yaniv:
Create init code (task 1)
Create init SQL query (task 2)
Make the code more modular and maintainable , follows the single responsibility principle better
Improve the genrated data code (task 1)


LLM :
Modify the code to ensure a more realistic distribution of the data
Validate distribution and Print validation info.
Create git ignor file 
Improve the output formatting
Make any other enhancements to the code


Task 1 :

main.py

open terminal :
make all




Task 2 : 

feature_table.sql 

I started with init solution and decided to use  Window Function 
I asked the LLM for Alternative Solutions to validae more ideas and maybe better solution , in addtion the solution didnt mention the dataset size and  i added part to handle large dataset and consider using partitioning.

Let's break down exactly how our specific query is processed:

```sql
WITH daily_counts AS (
    SELECT 
        transaction_id,
        user_id,
        date,
        COUNT(*) OVER (
            PARTITION BY user_id 
            ORDER BY date 
            RANGE BETWEEN INTERVAL '7 days' PRECEDING AND INTERVAL '1 day' PRECEDING
        ) as transactions_last_7_days
    FROM transactions
)
```

### Step-by-Step Execution

1. **Initial Data Access**
   - Database first accesses the transactions table
   - If using our recommended index (user_id, date):
     ```sql
     CREATE INDEX idx_trans_user_date ON transactions(user_id, date);
     ```
   - Data is read in index order, already partially sorted

2. **Partitioning**
   - Data is divided into partitions by user_id
   - Example for user 'becf-457e':
     ```
     transaction_id  | date       
     ef05-4247      | 2020-01-01
     c8d1-40ca      | 2020-01-05
     fc2b-4b36      | 2020-01-07
     3725-48c4      | 2020-01-15
     ```

3. **Window Frame Processing**
   For each row, the database:
   - Positions the window (7 days before, excluding current day)
   - Counts transactions in that window
   
   Example calculation for 2020-01-07:
   ```
   Window start: 2020-01-01 (7 days before)
   Window end:   2020-01-06 (1 day before)
   Count: 1 transaction (on 2020-01-05)
   ```

4. **Memory Management**
   - For each user partition:
     * Keeps track of current window boundaries
     * Maintains count of transactions in window
     * Slides window as it processes each row

5. **Result Assembly**
   ```sql
   SELECT * FROM daily_counts
   ORDER BY user_id, date;
   ```
   - Results are sorted by user_id and date
   - Final output format:
     ```
     transaction_id | user_id    | date       | transactions_last_7_days
     ef05-4247     | becf-457e  | 2020-01-01 | 0
     c8d1-40ca     | becf-457e  | 2020-01-05 | 1
     fc2b-4b36     | becf-457e  | 2020-01-07 | 2
     ```

### Performance Analysis

1. **Time Efficiency**
   - For each partition (user):
     * Initial sort: O(n log n) where n = transactions per user
     * Window calculation: O(n) as window slides forward
   - Total complexity: O(N log N) where N = total transactions

2. **Memory Usage**
   - Per partition:
     * Window buffer: ~7 days worth of transactions
     * Sort buffer: transactions for one user
   - Temporary storage for window calculations

3. **I/O Pattern**
   - Sequential reads within each partition
   - One write pass for final results
   - Index helps reduce initial I/O

### Key Optimizations in Action

1. **Partition Processing**
   ```
   User1's transactions → Process window → Output
   User2's transactions → Process window → Output
   ```
   - Each user's data processed independently
   - Enables parallel processing

2. **Window Frame Movement**
   ```
   Day 1: [       ] → count=0
   Day 5: [Day 1  ] → count=1
   Day 7: [Day 1,5] → count=2
   ```
   - Efficient sliding window implementation
   - Only updates changed boundaries

3. **Data Locality**
   - Related transactions stay together
   - Reduces memory page faults
   - Better cache utilization

 Task 3 - Dimension Deduplication

 when approche this task i understod that in order to complete the task sucessfully I will need to take in considration those  
   - Single table scan
   - Minimal memory usage
   - use window function processing

   I come up with dimension_deduplication.sql file that use window function to compare each row with the next row and identify the change points.

   I know that the solution is not the best and i can do better, then i asked the LLM for review my solution and improve it and then I got dimension_deduplication_optimized.sql .
   I review the solution and i like the logic and the approach.

