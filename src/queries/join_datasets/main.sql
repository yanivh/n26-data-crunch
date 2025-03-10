-- Join transactions with users and agreement dimension
WITH valid_transactions AS (
    SELECT 
        t.transaction_id,
        t.date as transaction_date,
        t.user_id,
        t.is_blocked,
        t.transaction_amount,
        t.transaction_category_id,
        u.is_active,
        a.product_id,
        a.interest_rate
    FROM transactions t
    LEFT JOIN users u ON t.user_id = u.user_id
    LEFT JOIN dim_dep_agreement a ON 
        t.user_id = a.client_id AND
        t.date >= a.actual_from_dt AND
        t.date < CAST(a.actual_to_dt AS DATE)
)
SELECT 
    transaction_id,
    transaction_date,
    user_id,
    is_blocked,
    transaction_amount,
    transaction_category_id,
    is_active,
    product_id,
    interest_rate
FROM valid_transactions
ORDER BY transaction_date, transaction_id; 