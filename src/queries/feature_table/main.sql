-- Feature Table Computation Query
-- Computes the number of transactions per user within the previous 7 days

-- Solution using Window Functions (Most Efficient)
WITH daily_counts AS (
    SELECT 
        transaction_id,
        user_id,
        CAST(date AS DATE) as date,
        CAST(
            COALESCE(
                COUNT(*) OVER (
                    PARTITION BY user_id 
                    ORDER BY CAST(date AS DATE)
                    ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING
                ),
                0
            ) AS INTEGER
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