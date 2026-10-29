-- Exact business-field duplicates are collapsed without changing raw data.
-- The preceding duplicate investigation confirmed no conflicting events.
-- Assumption: each rental day is billed at the reference daily rate.

WITH unique_events AS (
    SELECT DISTINCT
        event_id,
        event_date,
        equipment_id,
        equipment_type,
        location_id,
        status,
        rental_days,
        billed_amount_cents,
        source_batch
    FROM transactions
),
reconciled AS (
    SELECT
        t.event_id,
        t.billed_amount_cents,
        t.rental_days * r.daily_rate_cents AS expected_amount_cents,
        t.billed_amount_cents
            - (t.rental_days * r.daily_rate_cents) AS variance_cents
    FROM unique_events AS t
    LEFT JOIN rates AS r
        ON t.equipment_type = r.equipment_type
)
SELECT
    COUNT(*) AS unique_events,
    SUM(CASE WHEN expected_amount_cents IS NULL THEN 1 ELSE 0 END)
        AS unmatched_rate_events,
    SUM(CASE WHEN variance_cents > 0 THEN 1 ELSE 0 END)
        AS overcharged_events,
    SUM(CASE WHEN variance_cents < 0 THEN 1 ELSE 0 END)
        AS undercharged_events,
    SUM(CASE WHEN variance_cents > 0 THEN variance_cents ELSE 0 END)
        AS overcharge_cents,
    SUM(CASE WHEN variance_cents < 0 THEN -variance_cents ELSE 0 END)
        AS undercharge_cents,
    ROUND(
        100.0 * SUM(CASE WHEN variance_cents != 0 THEN 1 ELSE 0 END)
        / NULLIF(COUNT(expected_amount_cents), 0),
        2
    ) AS discrepancy_pct_of_rate_matched_events
FROM reconciled;
