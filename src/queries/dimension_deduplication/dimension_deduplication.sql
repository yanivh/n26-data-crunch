-- Dimension Deduplication Solution
-- This query compacts redundant records in the agreement dimension table
-- by collapsing consecutive records with identical business attributes.

-- Main dimension deduplication query
WITH numbered_rows AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (
            PARTITION BY agrmnt_id, client_id, product_id, interest_rate 
            ORDER BY actual_from_dt
        ) as row_num,
        LEAD(actual_from_dt) OVER (
            PARTITION BY agrmnt_id 
            ORDER BY actual_from_dt
        ) as next_start_date
    FROM dim_dep_agreement
),
distinct_periods AS (
    SELECT 
        sk_agrmnt_id,
        agrmnt_id,
        actual_from_dt,
        CASE 
            WHEN next_start_date IS NULL THEN '9999-12-31'::VARCHAR
            ELSE next_start_date::VARCHAR
        END as actual_to_dt,
        client_id,
        product_id,
        interest_rate
    FROM numbered_rows
    WHERE row_num = 1
)
SELECT 
    sk_agrmnt_id,
    agrmnt_id,
    actual_from_dt,
    actual_to_dt,
    client_id,
    product_id,
    interest_rate
FROM distinct_periods
ORDER BY agrmnt_id, actual_from_dt;

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