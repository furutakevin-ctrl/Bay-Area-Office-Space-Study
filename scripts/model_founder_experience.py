from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed"
BASE = DATA / "startup_office_seed_funding.csv"
ENRICHMENT = DATA / "founder_experience_enrichment.csv"


def fit_model(df: pd.DataFrame, terms: list[str], name: str) -> pd.DataFrame:
    X = pd.DataFrame({"intercept": 1.0}, index=df.index)
    for term in terms:
        if term == "founder_experience":
            X[term] = df["founder_prior_startup_experience"]
        elif term == "shared_office":
            X[term] = (df["office_space_type"] == "shared").astype(int)
        elif term.startswith("year_"):
            year = int(term.split("_")[1])
            X[term] = (df["seed_funding_year"] == year).astype(int)

    y = np.log(df["seed_funding_usd"].to_numpy())
    X_values = X.to_numpy()
    beta, _, _, _ = np.linalg.lstsq(X_values, y, rcond=None)
    residuals = y - X_values @ beta
    n, k = X_values.shape
    covariance = (residuals @ residuals) / (n - k) * np.linalg.inv(X_values.T @ X_values)
    se = np.sqrt(np.diag(covariance))
    t_values = beta / se
    p_values = 2 * stats.t.sf(np.abs(t_values), df=n - k)
    critical = stats.t.ppf(0.975, df=n - k)

    result = pd.DataFrame(
        {
            "model": name,
            "term": X.columns,
            "coefficient_log_scale": beta,
            "standard_error": se,
            "t_statistic": t_values,
            "p_value": p_values,
            "ci_low": beta - critical * se,
            "ci_high": beta + critical * se,
            "percent_difference": (np.exp(beta) - 1) * 100,
        }
    )
    return result


def main() -> None:
    base = pd.read_csv(BASE)
    enrichment = pd.read_csv(ENRICHMENT)
    df = base.merge(enrichment, on="company", how="left", validate="one_to_one")
    df["founder_prior_startup_experience"] = pd.to_numeric(
        df["founder_prior_startup_experience"], errors="coerce"
    )
    df["seed_funding_year"] = pd.to_numeric(df["seed_funding_year"])
    df.to_csv(DATA / "startup_office_seed_funding_augmented.csv", index=False)

    summary = (
        df.groupby("founder_prior_startup_experience", as_index=False)["seed_funding_usd"]
        .agg(
            company_count="count",
            mean_funding_usd="mean",
            median_funding_usd="median",
            minimum_funding_usd="min",
            maximum_funding_usd="max",
        )
        .rename(columns={"founder_prior_startup_experience": "prior_founder_experience"})
    )
    summary.to_csv(DATA / "founder_experience_funding_summary.csv", index=False)

    terms = ["founder_experience", "year_2024", "year_2025", "year_2026"]
    adjusted_terms = ["founder_experience", "shared_office", "year_2024", "year_2025", "year_2026"]
    coefficients = pd.concat(
        [fit_model(df, terms, "founder_experience_year_adjusted"), fit_model(df, adjusted_terms, "founder_experience_office_year_adjusted")],
        ignore_index=True,
    )
    coefficients.to_csv(DATA / "founder_experience_model_coefficients.csv", index=False)

    print("SUMMARY")
    print(summary.to_string(index=False))
    print("\nCOEFFICIENTS")
    print(coefficients.to_string(index=False))


if __name__ == "__main__":
    main()
