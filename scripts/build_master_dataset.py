from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed"
BASE = DATA / "startup_office_seed_funding.csv"
ENRICHMENT = DATA / "founder_experience_enrichment.csv"
MASTER = DATA / "startup_office_seed_funding_master.csv"


def main() -> None:
    base = pd.read_csv(BASE)
    founder = pd.read_csv(ENRICHMENT)
    df = base.merge(founder, on="company", how="left", validate="one_to_one")

    df["seed_funding_usd"] = pd.to_numeric(df["seed_funding_usd"], errors="coerce")
    df["seed_funding_year"] = pd.to_numeric(df["seed_funding_year"], errors="coerce").astype("Int64")
    df["prior_founder_experience"] = pd.to_numeric(
        df["founder_prior_startup_experience"], errors="coerce"
    ).astype("Int64")
    df["shared_office"] = (df["office_space_type"] == "shared").astype("Int64")
    df["private_office"] = (df["office_space_type"] == "private").astype("Int64")
    df["log_seed_funding"] = np.log(df["seed_funding_usd"])
    for column in ["founder_experience_notes", "founder_names", "prior_startup_names"]:
        df[column] = df[column].astype("string").str.replace('"""', "", regex=False)

    columns = [
        "company",
        "city",
        "office_address",
        "office_space_type",
        "shared_office",
        "private_office",
        "office_evidence_status",
        "seed_funding_usd",
        "seed_funding_year",
        "funding_round_label",
        "log_seed_funding",
        "funding_evidence_status",
        "founder_names",
        "prior_founder_experience",
        "prior_startup_names",
        "founder_experience_notes",
        "evidence_status",
        "source_urls",
        "founder_experience_sources",
        "evidence_notes",
    ]
    df[columns].sort_values("company").to_csv(MASTER, index=False)

    print(f"Created {MASTER}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(columns)}")
    print(f"Duplicates: {df['company'].duplicated().sum()}")
    print(f"Missing prior-founder values: {df['prior_founder_experience'].isna().sum()}")


if __name__ == "__main__":
    main()
