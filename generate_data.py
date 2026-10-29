"""Create a reproducible, entirely fictional logistics database."""

import json
import random
import sqlite3
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
DATABASE = DATA_DIR / "logistics.db"
BASE_EVENTS = 50_000
SEED = 97


def main():
    # Avoid accidentally overwriting an existing investigation database.
    if DATABASE.exists():
        raise FileExistsError(
            "data/logistics.db already exists. "
            "Use a fresh extracted repository to regenerate."
        )

    DATA_DIR.mkdir(exist_ok=True)
    rng = random.Random(SEED)

    locations = [
        (f"L{i:02d}", f"Fictional Depot {i:02d}")
        for i in range(1, 21)
    ]
    rates = [
        ("standard", 8000),
        ("refrigerated", 12000),
        ("specialty", 15000),
    ]
    rate_lookup = dict(rates)

    counts = {
        "billing_overcharge_events": 0,
        "missing_status_events": 0,
        "invalid_status_events": 0,
        "location_alias_events": 0,
        "unknown_location_events": 0,
        "missing_location_events": 0,
        "extra_duplicate_rows": 0,
    }

    records = []
    start_date = date(2026, 1, 1)

    for i in range(1, BASE_EVENTS + 1):
        equipment_type = rng.choice(list(rate_lookup))
        rental_days = rng.randint(1, 10)
        billed_cents = rental_days * rate_lookup[equipment_type]
        location_id = rng.choice(locations)[0]
        status = "completed"
        event_date = start_date + timedelta(days=rng.randrange(181))

        # Separate issue groups simplify independent verification.
        issue_slot = i % 1000

        if issue_slot == 1:
            billed_cents += 2500
            counts["billing_overcharge_events"] += 1
        elif issue_slot == 2:
            status = None
            counts["missing_status_events"] += 1
        elif issue_slot == 3:
            status = "COMPLETE?"
            counts["invalid_status_events"] += 1
        elif issue_slot == 4:
            location_id = location_id.lower()
            counts["location_alias_events"] += 1
        elif issue_slot == 5:
            location_id = "L99"
            counts["unknown_location_events"] += 1
        elif issue_slot == 6:
            location_id = None
            counts["missing_location_events"] += 1

        # Grain: one rental event. Equipment can appear in many events.
        event = (
            f"EVT-{i:06d}",
            event_date.isoformat(),
            f"EQ-{rng.randint(1, 5000):05d}",
            equipment_type,
            location_id,
            status,
            rental_days,
            billed_cents,
            f"BATCH-{event_date:%Y%m}",
        )
        records.append((len(records) + 1,) + event)

        # Replay an otherwise clean event with a new received-row ID.
        if i % 100 == 0:
            records.append((len(records) + 1,) + event)
            counts["extra_duplicate_rows"] += 1

    connection = sqlite3.connect(DATABASE)
    try:
        schema = (ROOT / "sql/00_schema.sql").read_text(encoding="utf-8")
        connection.executescript(schema)

        with connection:
            connection.executemany(
                "INSERT INTO locations VALUES (?, ?)", locations
            )
            connection.executemany(
                "INSERT INTO rates VALUES (?, ?)", rates
            )
            connection.executemany(
                "INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                records,
            )

        actual_rows = connection.execute(
            "SELECT COUNT(*) FROM transactions"
        ).fetchone()[0]
    finally:
        connection.close()

    if actual_rows != BASE_EVENTS + counts["extra_duplicate_rows"]:
        raise AssertionError("Unexpected database row count.")

    manifest = {
        "dataset": "Entirely synthetic; not employer data",
        "seed": SEED,
        "base_events": BASE_EVENTS,
        "raw_rows": actual_rows,
        "locations": len(locations),
        "date_range": ["2026-01-01", "2026-06-30"],
        "currency": "USD",
        "amount_unit": "integer cents",
        "injected_issues": counts,
        "injected_overcharge_cents": (
            counts["billing_overcharge_events"] * 2500
        ),
        "verification_note": (
            "Generator counts are ground truth for this simulation. "
            "Investigative SQL must verify them independently."
        ),
    }

    (DATA_DIR / "generation_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )

    print(f"Created {actual_rows:,} raw rows from {BASE_EVENTS:,} events.")
    print("Created 20 fictional locations and 3 equipment rates.")
    print("Database: data/logistics.db")
    print("Known injected issues: data/generation_manifest.json")


if __name__ == "__main__":
    main()
