-- Report event-level exceptions by month.
-- An event with several issues counts once in any_exception_events.

WITH unique_events AS (
    SELECT DISTINCT
        event_id, event_date, equipment_id, equipment_type,
        location_id, status, rental_days, billed_amount_cents,
        source_batch
    FROM transactions
),
flagged AS (
    SELECT
        t.event_id,
        SUBSTR(t.event_date, 1, 7) AS event_month,
        CASE
            WHEN r.equipment_type IS NULL THEN 1
            WHEN t.billed_amount_cents !=
                 t.rental_days * r.daily_rate_cents THEN 1
            ELSE 0
        END AS billing_exception,
        CASE
            WHEN t.status IS NULL
                 OR t.status NOT IN ('completed', 'cancelled')
                THEN 1
            ELSE 0
        END AS status_exception,
        CASE
            WHEN l.location_id IS NULL THEN 1
            ELSE 0
        END AS location_exception
    FROM unique_events AS t
    LEFT JOIN rates AS r
        ON t.equipment_type = r.equipment_type
    LEFT JOIN locations AS l
        ON t.location_id = l.location_id
)
SELECT
    event_month,
    COUNT(*) AS total_events,
    SUM(billing_exception) AS billing_exception_events,
    SUM(status_exception) AS status_exception_events,
    SUM(location_exception) AS location_exception_events,
    SUM(
        CASE
            WHEN billing_exception = 1
                 OR status_exception = 1
                 OR location_exception = 1
                THEN 1
            ELSE 0
        END
    ) AS any_exception_events,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN billing_exception = 1
                     OR status_exception = 1
                     OR location_exception = 1
                    THEN 1
                ELSE 0
            END
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS exception_pct
FROM flagged
GROUP BY event_month
ORDER BY event_month;
