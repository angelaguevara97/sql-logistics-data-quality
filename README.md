# SQL Logistics Data Quality

A personal analyst case study investigating duplicate logistics events, billing discrepancies, and operational data-quality issues using entirely synthetic data.

**Status:** Under construction. Dataset generation, SQL queries, and verified findings will be added as completed.

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
