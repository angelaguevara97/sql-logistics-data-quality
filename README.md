# SQL Logistics Data Quality

A personal analyst case study investigating duplicate logistics events, billing discrepancies, and operational data-quality issues using entirely synthetic data.

**Status:** Working, reproducible case study. Generates 50,500 synthetic intake rows representing 50,000 rental events, runs five SQL investigations, and exports results to CSV.

## Business Problem

A fictional equipment-leasing company receives logistics events through an EDI-style integration and uses transaction records to support billing.

Repeated event transmissions, inconsistent locations, missing statuses, and incorrect charges can undermine reporting and create reconciliation work.

The investigation asks:

- Which records are repeated transmissions of the same business event?
- Which charges differ from the agreed rate and billable duration?
- Where are statuses or location references missing or invalid?
- How do exceptions vary across locations and time?
- What controls would prevent these issues from recurring?

## Investigation Approach

1. Generate a reproducible synthetic dataset with at least 50,000 transaction records.
2. Preserve raw records and document their expected grain.
3. Profile missing values, statuses, and location references.
4. Detect repeated business events without confusing them with legitimate separate transactions.
5. Reconcile billed amounts against reference rates and durations.
6. Calculate exception rates and monthly trends.
7. Compare SQL findings with the generator's known issue counts.

Known issue counts serve as a verification reference. They are not evidence of real company performance.

## Planned Data Model

| Table | Purpose |
|---|---|
| locations | Canonical fictional operating locations |
| rates | Agreed daily rates by equipment type |
| transactions | Raw logistics and billing records, including intentional issues |

A transaction represents a billable equipment rental event. Each source row has a unique record ID; an event ID identifies the underlying business event and may repeat after retransmission.

All amounts use USD. Billing rules and rounding assumptions will be documented with the dataset.

## SQL Scope

The case study will demonstrate:

- SELECT and WHERE
- JOINs
- GROUP BY and aggregate functions
- CASE expressions
- Common table expressions
- Duplicate detection
- Billing reconciliation
- Exception-rate calculations
- Monthly trend analysis

SQLite will provide a lightweight local database. Python will generate synthetic data and run SQL; the investigation logic will remain visible in SQL files.

## Intended Deliverables

- Reproducible synthetic-data generator
- Database schema and data dictionary
- Numbered SQL investigation files
- Exported query results
- Verified findings and business recommendations
- Run instructions and query explanations

## Connection to My Experience

This project is inspired by the types of reconciliation and duplicate-record investigations I encountered as a data analyst.

The company, records, rates, locations, and findings are fictional. No former employer's data, source code, or internal documentation is used.

## My Role

I am defining the business questions, data-quality rules, SQL investigation, validation approach, and recommendations, using AI-assisted development to support implementation.

The purpose is to demonstrate analytical judgment and explainable SQL rather than claim advanced software-engineering experience.

## Success Criteria

A reviewer should be able to reproduce the dataset, inspect the SQL, verify the reported findings, and understand how each recommendation follows from the evidence.

Financial results will be described as synthetic billing discrepancies or potential exposure, not recovered revenue or proven business savings.
## Run the Case Study

Requires Python 3 with its standard-library SQLite module. No external packages, credentials, or data downloads are needed.

Download and extract this repository. Open a terminal in the extracted folder and run these commands in order:

```bash
python3 generate_data.py
python3 run_analysis.py
```

The generator creates `data/logistics.db` and `data/generation_manifest.json`. It refuses to overwrite an existing database.

The analysis runner opens the database read-only and exports five CSV files into `results/`. Successful runs overwrite those result files.

The generator uses a fixed random seed. The findings below were verified on macOS; the generator manifest records the intended issue counts.

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
| Missing statuses | 50 |
| Invalid statuses | 50 |
| Location formatting aliases | 50 |
| Missing locations | 50 |
| Unknown locations | 50 |
| Unique events with billing, status, or location exceptions | 300 |
| Overall event exception rate | 0.60% |

The 300 exception events exclude the 500 identical replays, which were analyzed separately.

The USD 1,250 represents synthetic billing variance under the stated rate rules, not recovered revenue or realized savings.

## Investigation Files

| Step | SQL | Exported result |
|---|---|---|
| Profile raw intake | [Data profile](sql/01_data_profile.sql) | [CSV](results/01_data_profile.csv) |
| Distinguish identical replays from conflicts | [Duplicate events](sql/02_duplicate_events.sql) | [CSV](results/02_duplicate_events.csv) |
| Compare charges with reference rates | [Billing reconciliation](sql/03_billing_reconciliation.sql) | [CSV](results/03_billing_reconciliation.csv) |
| Classify location references | [Location quality](sql/04_location_quality.sql) | [CSV](results/04_location_quality.csv) |
| Compare monthly exception rates | [Monthly trends](sql/05_monthly_trends.sql) | [CSV](results/05_monthly_trends.csv) |

Additional files:

- [Database schema](sql/00_schema.sql)
- [Synthetic-data generator](generate_data.py)
- [Analysis runner](run_analysis.py)
- [Findings, interpretation, and recommended controls](docs/findings.md)

## Analytical Decisions

- Preserve raw intake records rather than deleting duplicates.
- Compare business details before treating repeated event IDs as identical replays.
- Collapse exact business-record copies for event-level analysis.
- Use LEFT JOINs to retain unmatched reference values.
- Store money as integer cents.
- Count an event once when it has any exception.
- Compare monthly rates alongside counts.
- Distinguish formatting aliases from unknown or missing locations.

## Recommended Solution

Introduce duplicate-processing controls, validate statuses and location references at intake, and reconcile proposed charges against agreed rates before billing.

Route conflicting records and unresolved references to an exception queue. Monitor exception counts and rates to assess whether corrective actions reduce recurring problems.

## Limits

This is a controlled simulation with known injected issues. Matching the generator counts verifies the demonstrated queries; it does not establish accuracy on unseen business data.

Billing assumes rental days multiplied by a fixed equipment rate. Taxes, discounts, contract changes, and service-record verification are outside scope.

Monthly variation comes from synthetic date assignments and does not establish seasonality or an operational cause.

The queries assume no conflicting versions remain when producing event-level results. The duplicate investigation must be reviewed before interpreting later outputs.
