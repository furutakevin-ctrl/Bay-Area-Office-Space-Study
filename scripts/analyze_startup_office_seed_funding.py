from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "processed" / "startup_office_seed_funding.csv"
OUTPUT = ROOT / "data" / "processed"


def main() -> None:
    df = pd.read_csv(INPUT)
    df["seed_funding_usd"] = pd.to_numeric(df["seed_funding_usd"], errors="coerce")
    df["seed_funding_year"] = pd.to_numeric(df["seed_funding_year"], errors="coerce").astype("Int64")

    audit = {
        "row_count": len(df),
        "duplicate_company_count": int(df["company"].str.casefold().duplicated().sum()),
        "missing_value_count": int(df.isna().sum().sum()),
        "invalid_funding_count": int(df["seed_funding_usd"].isna().sum()),
        "invalid_year_count": int((~df["seed_funding_year"].between(2023, 2026)).sum()),
        "shared_count": int((df["office_space_type"] == "shared").sum()),
        "private_count": int((df["office_space_type"] == "private").sum()),
    }
    pd.DataFrame([audit]).to_csv(OUTPUT / "startup_office_seed_funding_audit.csv", index=False)

    summary = (
        df.groupby("office_space_type", as_index=False)["seed_funding_usd"]
        .agg(
            company_count="count",
            mean_funding_usd="mean",
            median_funding_usd="median",
            minimum_funding_usd="min",
            maximum_funding_usd="max",
            standard_deviation_usd="std",
        )
    )
    summary.to_csv(OUTPUT / "startup_office_seed_funding_summary.csv", index=False)

    yearly = (
        df.groupby(["seed_funding_year", "office_space_type"], as_index=False)["seed_funding_usd"]
        .agg(company_count="count", median_funding_usd="median", mean_funding_usd="mean")
    )
    yearly.to_csv(OUTPUT / "startup_office_seed_funding_by_year.csv", index=False)

    print("AUDIT")
    for key, value in audit.items():
        print(f"{key}: {value}")
    print("\nSUMMARY")
    print(summary.to_string(index=False))
    print("\nBY YEAR")
    print(yearly.to_string(index=False))


if __name__ == "__main__":
    main()
