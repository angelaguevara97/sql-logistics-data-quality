"""Run saved investigation queries and export reproducible CSV results."""

import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATABASE = ROOT / "data/logistics.db"
RESULTS = ROOT / "results"

QUERIES = [
    "01_data_profile",
    "02_duplicate_events",
    "03_billing_reconciliation",
    "04_location_quality",
    "05_monthly_trends",
]


def main():
    if not DATABASE.is_file():
        raise FileNotFoundError(
            "Database missing. Run python3 generate_data.py first."
        )

    # Read and execute every query before writing any result files.
    outputs = {}
    database_uri = DATABASE.as_uri() + "?mode=ro"

    with sqlite3.connect(database_uri, uri=True) as connection:
        for name in QUERIES:
            query = (ROOT / "sql" / f"{name}.sql").read_text(
                encoding="utf-8"
            )
            cursor = connection.execute(query)
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()
            outputs[name] = (columns, rows)

    RESULTS.mkdir(exist_ok=True)

    for name, (columns, rows) in outputs.items():
        destination = RESULTS / f"{name}.csv"
        with destination.open("w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(columns)
            writer.writerows(rows)

        print(f"{name}: exported {len(rows)} result row(s)")

    print("Results saved in results/. Source database unchanged.")


if __name__ == "__main__":
    main()
