"""Print selected rows of the published experiment observations (standard library)."""

import argparse
import csv
from pathlib import Path


RESULTS = Path(__file__).resolve().parents[1] / "results" / "observations.csv"


def main() -> None:
    with RESULTS.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("study", choices=sorted({row["study"] for row in rows}))
    parser.add_argument("--metric", help="metric name shown in the CSV (e.g. mean_score)")
    args = parser.parse_args()
    selected = [row for row in rows if row["study"] == args.study]
    available = sorted({row["metric"] for row in selected})
    if args.metric is not None:
        if args.metric not in available:
            parser.error("metrics for this study: " + ", ".join(available))
        selected = [row for row in selected if row["metric"] == args.metric]
    for row in selected:
        print(f"{row['condition']} | {row['metric']} = {float(row['value']):g} "
              f"{row['unit']} | {row['scope']}")


if __name__ == "__main__":
    main()
