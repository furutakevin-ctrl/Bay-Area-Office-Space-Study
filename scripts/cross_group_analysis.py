from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed"
INPUT = DATA / "startup_office_seed_funding_master.csv"
OUTPUT = DATA / "four_group_funding_comparison.csv"


def main() -> None:
    df = pd.read_csv(INPUT)
    df["prior_founder_experience_label"] = df["prior_founder_experience"].map(
        {0: "No documented prior experience", 1: "Prior founder experience"}
    )
    summary = (
        df.groupby(["office_space_type", "prior_founder_experience", "prior_founder_experience_label"], as_index=False)
        .agg(
            company_count=("company", "count"),
            mean_seed_funding_usd=("seed_funding_usd", "mean"),
            median_seed_funding_usd=("seed_funding_usd", "median"),
            mean_log_seed_funding=("log_seed_funding", "mean"),
            minimum_seed_funding_usd=("seed_funding_usd", "min"),
            maximum_seed_funding_usd=("seed_funding_usd", "max"),
        )
    )
    summary["group_label"] = (
        summary["office_space_type"].str.title()
        + " office / "
        + summary["prior_founder_experience_label"]
    )

    baseline = summary.loc[
        (summary["office_space_type"] == "private")
        & (summary["prior_founder_experience"] == 0),
        "median_seed_funding_usd",
    ].iloc[0]
    summary["median_ratio_vs_private_no_experience"] = summary["median_seed_funding_usd"] / baseline
    summary = summary.sort_values("median_seed_funding_usd", ascending=False)
    summary.to_csv(OUTPUT, index=False)

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
