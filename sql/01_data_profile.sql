-- Profile raw intake before cleaning.
-- Raw-row counts can include repeated transmissions.

SELECT
    COUNT(*) AS raw_rows,
    COUNT(DISTINCT event_id) AS distinct_events,
    COUNT(*) - COUNT(DISTINCT event_id) AS extra_event_rows,
    MIN(event_date) AS earliest_event_date,
    MAX(event_date) AS latest_event_date,
    SUM(CASE WHEN status IS NULL THEN 1 ELSE 0 END)
        AS missing_status_rows,
    SUM(
        CASE
            WHEN status IS NOT NULL
                 AND status NOT IN ('completed', 'cancelled')
            THEN 1 ELSE 0
        END
    ) AS invalid_status_rows,
    SUM(CASE WHEN location_id IS NULL THEN 1 ELSE 0 END)
        AS missing_location_rows
FROM transactions;
