# Investigation Findings

## Executive Summary

SQL analysis of 50,500 synthetic intake rows identified 50,000 underlying rental events.

The investigation found 500 identical event replays and 300 unique events with billing, status, or location exceptions. Billing reconciliation identified USD 1,250 in synthetic overcharges.

All findings describe generated fictional data, not an actual company's performance.

## Verified Results

| Check | Observed result |
|---|---:|
| Raw intake rows | 50,500 |
| Distinct rental events | 50,000 |
| Extra replay rows | 500 |
| Repeated event IDs with identical business details | 500 |
| Conflicting event IDs | 0 |
| Events without a matching reference rate | 0 |
| Overcharged events | 50 |
| Undercharged events | 0 |
| Total overcharge | USD 1,250 |
| Missing status | 50 |
| Invalid status | 50 |
| Exact location matches | 49,850 |
| Location formatting aliases | 50 |
| Missing locations | 50 |
| Unknown locations | 50 |
| Unique events with any billing, status, or location exception | 300 |

These counts match the issues intentionally introduced by the generator.

## Monthly Trends

| Month | Events | Billing exceptions | Status exceptions | Location exceptions | Any exception | Exception rate |
|---|---:|---:|---:|---:|---:|---:|
| 2026-01 | 8,606 | 12 | 19 | 33 | 64 | 0.74% |
| 2026-02 | 7,584 | 6 | 17 | 17 | 40 | 0.53% |
| 2026-03 | 8,670 | 7 | 18 | 25 | 50 | 0.58% |
| 2026-04 | 8,357 | 12 | 18 | 27 | 57 | 0.68% |
| 2026-05 | 8,580 | 6 | 14 | 27 | 47 | 0.55% |
| 2026-06 | 8,203 | 7 | 14 | 21 | 42 | 0.51% |
| Total | 50,000 | 50 | 100 | 150 | 300 | 0.60% |

Dates were assigned by a seeded random generator. Monthly variation is a property of this simulation; no operational or seasonal cause can be inferred.

## Investigation Decisions

### Separate received rows from business events

A unique record ID identifies a received row. The event ID identifies the underlying rental.

Repeated event IDs were compared across business fields before deduplication. All 500 repeated events had identical details, so subsequent queries collapsed exact copies without modifying the raw table.

If conflicting versions were present, they would require an explicit resolution policy before event-level findings could be trusted.

### Reconcile billing using reference rates

Expected charge equals rental days multiplied by the equipment's daily rate.

Fifty events were billed USD 25 above that expectation, totaling USD 1,250. All 50,000 events matched a rate, producing a billing discrepancy rate of 0.10%.

This measures arithmetic discrepancies under the simulation's billing rules. It does not account for taxes, discounts, negotiated adjustments, or verified service records.

### Distinguish location problems

Fifty lowercase location IDs matched canonical IDs after normalization. Another 50 were missing, and 50 referenced an unknown location.

Formatting differences can be handled through controlled normalization. Missing and unknown references require investigation; they should not be silently assigned to an arbitrary depot.

### Count affected events once

The monthly query uses an OR condition to count an event once if it has any exception.

The generator places the six issue types in separate event groups. Their counts therefore add to 300 in this dataset. That would not necessarily hold in real data, where issues can overlap.

## Recommended Controls

| Finding | Recommended control |
|---|---|
| Identical event replays | Use an event identifier and payload comparison to prevent repeated processing; preserve intake history |
| Conflicting event versions | Quarantine conflicts for review rather than choosing an arbitrary row |
| Billing variance | Compare proposed charges with agreed rates and durations before release |
| Missing or invalid status | Require a recognized status or route the record to an exception queue |
| Location formatting aliases | Apply documented normalization while preserving the original value |
| Missing or unknown locations | Validate against the reference table and assign an owner for correction |
| Ongoing exceptions | Monitor counts and rates by month and operating location |

## Business Impact and Limits

The analysis demonstrates how SQL can identify reporting inflation risks, isolate billing discrepancies, and organize corrective work.

The USD 1,250 is synthetic overcharge exposure under stated assumptions. It is not recovered revenue, realized savings, or a claim that customers were actually charged.

Duplicate replay rows were excluded from event-level reconciliation. Any separate financial effect from accidentally billing those replays was not quantified.

The dataset was deliberately constructed with known issues. Matching those counts verifies this demonstration; it does not establish detection accuracy on unseen operational data.

## Verification

The data profile, duplicate investigation, billing reconciliation, location classification, and monthly trend queries were executed against the generated SQLite database on macOS.

Results were reviewed against the generator's issue counts. Automated assertions and exported query-result files are not yet included.
