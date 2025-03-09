
-- Feature Table Computation Query
-- Computes the number of transactions per user within the previous 7 days

-- Solution using Window Functions (Most Efficient)
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
SELECT 
    transaction_id,
    user_id,
    date,
    transactions_last_7_days as "# Transactions within previous 7 days"
FROM daily_counts
ORDER BY user_id, date;

-- Alternative Solutions (commented for reference):

/*
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
*/

-- Recommended Index for optimal performance:
-- CREATE INDEX idx_trans_user_date ON transactions(user_id, date);

-- For large datasets, consider partitioning:
/*
CREATE TABLE transactions (
    transaction_id UUID,
    date DATE,
    user_id UUID,
    is_blocked BOOLEAN,
    transaction_amount INTEGER,
    transaction_category_id INTEGER
) PARTITION BY RANGE (date);
*/

-- For frequent access, consider materialized view:
/*
CREATE MATERIALIZED VIEW mv_weekly_transaction_stats AS
WITH daily_counts AS (
    -- query as above
)
SELECT * FROM daily_counts;

-- Refresh materialized view:
REFRESH MATERIALIZED VIEW mv_weekly_transaction_stats;
*/ 