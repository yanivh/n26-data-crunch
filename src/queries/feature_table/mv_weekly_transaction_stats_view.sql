-- Performance Optimizations for Feature Table

-- Recommended Index for optimal performance:
CREATE INDEX idx_trans_user_date ON transactions(user_id, date);

-- For large datasets, consider partitioning:
CREATE TABLE transactions (
    transaction_id UUID,
    date DATE,
    user_id UUID,
    is_blocked BOOLEAN,
    transaction_amount INTEGER,
    transaction_category_id INTEGER
) PARTITION BY RANGE (date);

-- For frequent access, consider materialized view:
CREATE MATERIALIZED VIEW mv_weekly_transaction_stats AS
WITH daily_counts AS (
    -- query as above
)
SELECT * FROM daily_counts;

-- Refresh materialized view:
REFRESH MATERIALIZED VIEW mv_weekly_transaction_stats; 