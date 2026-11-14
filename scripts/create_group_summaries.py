from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed"
INPUT = DATA / "startup_office_seed_funding_master.csv"


def summarize(df: pd.DataFrame, group_field: str, label_field: str) -> pd.DataFrame:
    result = (
        df.groupby(group_field, as_index=False)["seed_funding_usd"]
        .agg(
            company_count="count",
            mean_seed_funding_usd="mean",
            median_seed_funding_usd="median",
            minimum_seed_funding_usd="min",
            maximum_seed_funding_usd="max",
            standard_deviation_usd="std",
        )
        .rename(columns={group_field: label_field})
    )
    return result


def main() -> None:
    df = pd.read_csv(INPUT)
    office = summarize(df, "office_space_type", "group")
    office.insert(0, "grouping_variable", "office_space_type")

    founder = summarize(df, "prior_founder_experience", "group")
    founder["group"] = founder["group"].map({0: "No documented prior founder experience", 1: "Prior founder experience"})
    founder.insert(0, "grouping_variable", "prior_founder_experience")

    pd.concat([office, founder], ignore_index=True).to_csv(
        DATA / "seed_funding_group_summaries.csv", index=False
    )

    cross = (
        df.groupby(["office_space_type", "prior_founder_experience"], as_index=False)["seed_funding_usd"]
        .agg(company_count="count", mean_seed_funding_usd="mean", median_seed_funding_usd="median")
    )
    cross.to_csv(DATA / "seed_funding_office_founder_cross_summary.csv", index=False)


if __name__ == "__main__":
    main()
