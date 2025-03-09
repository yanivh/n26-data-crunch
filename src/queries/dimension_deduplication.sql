-- Dimension Deduplication Solution
-- This query compacts redundant records in the agreement dimension table
-- by collapsing consecutive records with identical business attributes.

WITH 
-- detect attribute changes by comparing with next record
changes AS (
    SELECT 
        sk_agrmnt_id,
        agrmnt_id,
        actual_from_dt,
        actual_to_dt,
        client_id,
        product_id,
        interest_rate,
        -- Compare current row with next row for same agreement
        CASE WHEN 
            LEAD(client_id) OVER w != client_id OR
            LEAD(product_id) OVER w != product_id OR
            LEAD(interest_rate) OVER w != interest_rate OR
            LEAD(agrmnt_id) OVER w IS NULL  -- Last record
        THEN 1 ELSE 0 END as is_change
    FROM dim_dep_agreement
    WINDOW w AS (PARTITION BY agrmnt_id ORDER BY actual_from_dt)
),

-- Group consecutive unchanged records
groups AS (
    SELECT 
        sk_agrmnt_id,
        agrmnt_id,
        actual_from_dt,
        actual_to_dt,
        client_id,
        product_id,
        interest_rate,
        SUM(is_change) OVER (
            PARTITION BY agrmnt_id 
            ORDER BY actual_from_dt
            ROWS UNBOUNDED PRECEDING
        ) as group_id
    FROM changes
)

-- Create final compacted table
SELECT 
    MIN(sk_agrmnt_id) as sk_agrmnt_id,  -- Keep earliest surrogate key
    agrmnt_id,
    MIN(actual_from_dt) as actual_from_dt,  -- Start of period
    MAX(actual_to_dt) as actual_to_dt,      -- End of period
    client_id,
    product_id,
    interest_rate
FROM groups
GROUP BY 
    agrmnt_id,
    group_id,
    client_id,
    product_id,
    interest_rate
ORDER BY 
    agrmnt_id,
    actual_from_dt;

/*

Example of how it works for agreement 101:
Original:
sk  agrmnt  from        to          client  product  rate
1   101     2015-01-01  2015-02-20  20      305     3.5%
2   101     2015-02-21  2015-05-17  20      345     4%
3   101     2015-05-18  2015-07-05  20      345     4%    <- Redundant
4   101     2015-07-06  2015-08-22  20      539     6%

Compacted Result:
sk  agrmnt  from        to          client  product  rate
1   101     2015-01-01  2015-02-20  20      305     3.5%
2   101     2015-02-21  2015-07-05  20      345     4%    <- Merged
4   101     2015-07-06  2015-08-22  20      539     6%
5   101     2015-08-23  9999-12-31  20      345     4%

*/ 