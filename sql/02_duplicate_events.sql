-- Compare business fields, excluding the unique received-row ID.
-- GROUP BY treats matching NULL values as one group.

WITH payload_groups AS (
    SELECT
        event_id,
        event_date,
        equipment_id,
        equipment_type,
        location_id,
        status,
        rental_days,
        billed_amount_cents,
        source_batch,
        COUNT(*) AS copies
    FROM transactions
    GROUP BY
        event_id,
        event_date,
        equipment_id,
        equipment_type,
        location_id,
        status,
        rental_days,
        billed_amount_cents,
        source_batch
),
event_summary AS (
    SELECT
        event_id,
        SUM(copies) AS received_rows,
        COUNT(*) AS distinct_payloads
    FROM payload_groups
    GROUP BY event_id
)
SELECT
    COUNT(*) AS repeated_event_ids,
    SUM(received_rows - 1) AS extra_rows,
    SUM(CASE WHEN distinct_payloads = 1 THEN 1 ELSE 0 END)
        AS identical_replay_events,
    SUM(CASE WHEN distinct_payloads > 1 THEN 1 ELSE 0 END)
        AS conflicting_event_ids
FROM event_summary
WHERE received_rows > 1;
