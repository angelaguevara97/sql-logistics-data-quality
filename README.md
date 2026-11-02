# SQL Logistics Data Quality

A personal analyst case study investigating duplicate logistics events, billing discrepancies, and operational data-quality issues using entirely synthetic data.

## Live Project

**[Open the Live Interactive Demo](https://angel-guevara-sql-logistics.streamlit.app/)**

The Streamlit case study presents the investigation visually while keeping SQL as the analytical centerpiece.

## Business Problem

A fictional equipment-leasing company receives logistics events through an EDI-style integration and uses transaction records to support billing. Repeated transmissions, inconsistent locations, missing statuses, and incorrect charges can undermine reporting and create reconciliation work.

The investigation asks which records are repeated transmissions, which charges differ from reference rates, where operational fields are missing or invalid, how exceptions change over time, and what controls could reduce recurring issues.

## Investigation Approach

1. Generate a reproducible synthetic dataset.
2. Preserve raw intake records and document their expected grain.
3. Profile missing values, statuses, and location references.
4. Detect repeated business events without confusing them with legitimate separate transactions.
5. Reconcile billed amounts against reference rates and durations.
6. Calculate exception rates and monthly trends.
7. Compare SQL findings with the generator's known issue counts.

## Verified Findings

| Measure | Result |
|---|---:|
| Raw intake rows | 50,500 |
| Distinct rental events | 50,000 |
| Identical replay events | 500 |
| Conflicting event IDs | 0 |
| Overcharged events | 50 |
| Synthetic overcharge total | USD 1,250 |
| Billing discrepancy rate | 0.10% |
| Unique events with core exceptions | 300 |
| Overall event exception rate | 0.60% |

The 300 exception events exclude the 500 identical replays, which are analyzed separately. The USD 1,250 represents synthetic billing variance, not recovered revenue or realized savings.

## SQL Scope

The case study demonstrates SELECT and WHERE, JOINs, GROUP BY and aggregates, CASE expressions, common table expressions, duplicate detection, billing reconciliation, exception-rate calculations, and monthly trend analysis.

SQLite provides the local database. Python generates synthetic data and runs the SQL while the investigation logic remains visible in the SQL files and live application.

## Investigation Files

| Step | SQL | Exported result |
|---|---|---|
| Profile raw intake | [Data profile](sql/01_data_profile.sql) | [CSV](results/01_data_profile.csv) |
| Distinguish identical replays from conflicts | [Duplicate events](sql/02_duplicate_events.sql) | [CSV](results/02_duplicate_events.csv) |
| Compare charges with reference rates | [Billing reconciliation](sql/03_billing_reconciliation.sql) | [CSV](results/03_billing_reconciliation.csv) |
| Classify location references | [Location quality](sql/04_location_quality.sql) | [CSV](results/04_location_quality.csv) |
| Compare monthly exception rates | [Monthly trends](sql/05_monthly_trends.sql) | [CSV](results/05_monthly_trends.csv) |

Additional files include the database schema, synthetic-data generator, analysis runner, and documented findings and recommendations.

## Analytical Decisions

- Preserve raw intake rather than deleting duplicate records.
- Compare business details before treating repeated event IDs as identical replays.
- Collapse exact business-record copies for event-level analysis.
- Use LEFT JOINs to retain unmatched reference values.
- Store money as integer cents.
- Count an event once when it has any core exception.
- Compare monthly rates alongside counts.
- Distinguish formatting aliases from unknown or missing locations.

## Recommended Controls

Introduce duplicate-processing controls, validate statuses and location references at intake, and reconcile proposed charges against agreed rates before billing. Route conflicting records and unresolved references to an exception queue and monitor exception counts and rates over time.

## Run Locally

Requires Python 3 with SQLite support.

```bash
python3 generate_data.py
python3 run_analysis.py
streamlit run app.py
```

## Data and Limitations

All company records, rates, locations, and findings are fictional. No former employer data, source code, or internal documentation is used.

This is a controlled simulation with known injected issues. Matching generator counts verifies the demonstrated queries but does not establish accuracy on unseen business data.

## Author

Angel Guevara
