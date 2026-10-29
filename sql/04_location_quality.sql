-- Compare raw location references with the canonical location table.
-- Normalization is diagnostic; raw records remain unchanged.

WITH unique_events AS (
    SELECT DISTINCT
        event_id, event_date, equipment_id, equipment_type,
        location_id, status, rental_days, billed_amount_cents,
        source_batch
    FROM transactions
),
classified AS (
    SELECT
        t.event_id,
        CASE
            WHEN t.location_id IS NULL
                 OR TRIM(t.location_id) = ''
                THEN 'missing'
            WHEN exact_location.location_id IS NOT NULL
                THEN 'exact_match'
            WHEN normalized_location.location_id IS NOT NULL
                THEN 'format_alias'
            ELSE 'unknown'
        END AS location_quality
    FROM unique_events AS t
    LEFT JOIN locations AS exact_location
        ON t.location_id = exact_location.location_id
    LEFT JOIN locations AS normalized_location
        ON UPPER(TRIM(t.location_id)) = normalized_location.location_id
)
SELECT
    location_quality,
    COUNT(*) AS event_count,
    ROUND(
        100.0 * COUNT(*) / (SELECT COUNT(*) FROM classified),
        2
    ) AS pct_of_unique_events
FROM classified
GROUP BY location_quality
ORDER BY location_quality;
