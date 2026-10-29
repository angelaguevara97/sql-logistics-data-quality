-- Synthetic logistics case study.
-- Raw transactions intentionally allow data-quality problems.
-- Reference tables use stricter constraints.

CREATE TABLE locations (
    location_id TEXT PRIMARY KEY,
    location_name TEXT NOT NULL
);

CREATE TABLE rates (
    equipment_type TEXT PRIMARY KEY,
    daily_rate_cents INTEGER NOT NULL CHECK (daily_rate_cents > 0)
);

CREATE TABLE transactions (
    record_id INTEGER PRIMARY KEY,
    event_id TEXT NOT NULL,
    event_date TEXT NOT NULL,
    equipment_id TEXT NOT NULL,
    equipment_type TEXT NOT NULL,
    location_id TEXT,
    status TEXT,
    rental_days INTEGER NOT NULL,
    billed_amount_cents INTEGER NOT NULL,
    source_batch TEXT NOT NULL
);

CREATE INDEX idx_transactions_event
    ON transactions (event_id);

CREATE INDEX idx_transactions_date
    ON transactions (event_date);
