-- Alternative Solutions for Feature Table Computation

-- Solution 1: Using Self-Join (More readable but less efficient)
WITH transaction_counts AS (
    SELECT 
        t1.transaction_id,
        t1.user_id,
        t1.date,
        COUNT(t2.transaction_id) as transactions_last_7_days
    FROM transactions t1
    LEFT JOIN transactions t2 ON 
        t1.user_id = t2.user_id AND
        t2.date >= t1.date - INTERVAL '7 days' AND
        t2.date < t1.date
    GROUP BY 
        t1.transaction_id,
        t1.user_id,
        t1.date
)
SELECT * FROM transaction_counts
ORDER BY user_id, date;

-- Solution 2: Using Correlated Subquery (Not recommended for large datasets)
WITH transaction_counts AS (
    SELECT
        t1.transaction_id,
        t1.user_id,
        t1.date,
        (
            SELECT COUNT(*)
            FROM transactions t2
            WHERE 
                t2.user_id = t1.user_id
                AND t2.date >= t1.date - INTERVAL '7 days'
                AND t2.date < t1.date
        ) AS transactions_last_7_days
    FROM transactions t1
)
SELECT * FROM transaction_counts
ORDER BY user_id, date; 