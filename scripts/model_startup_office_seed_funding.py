from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "processed" / "startup_office_seed_funding.csv"
OUTPUT = ROOT / "data" / "processed"


def main() -> None:
    df = pd.read_csv(INPUT)
    df["log_seed_funding"] = np.log(df["seed_funding_usd"])
    df["shared_office"] = (df["office_space_type"] == "shared").astype(int)

    # 2023 is the reference funding year.
    X = pd.DataFrame({"intercept": 1.0, "shared_office": df["shared_office"]})
    for year in [2024, 2025, 2026]:
        X[f"year_{year}"] = (df["seed_funding_year"] == year).astype(int)
    y = df["log_seed_funding"].to_numpy()
    X_values = X.to_numpy()

    beta, _, _, _ = np.linalg.lstsq(X_values, y, rcond=None)
    residuals = y - X_values @ beta
    n, k = X_values.shape
    covariance = (residuals @ residuals) / (n - k) * np.linalg.inv(X_values.T @ X_values)
    standard_errors = np.sqrt(np.diag(covariance))
    t_values = beta / standard_errors
    p_values = 2 * stats.t.sf(np.abs(t_values), df=n - k)
    critical = stats.t.ppf(0.975, df=n - k)

    coefficients = pd.DataFrame(
        {
            "term": X.columns,
            "coefficient_log_scale": beta,
            "standard_error": standard_errors,
            "t_statistic": t_values,
            "p_value": p_values,
            "ci_low": beta - critical * standard_errors,
            "ci_high": beta + critical * standard_errors,
        }
    )
    coefficients["percent_difference_vs_reference"] = np.nan
    shared_row = coefficients["term"] == "shared_office"
    coefficients.loc[shared_row, "percent_difference_vs_reference"] = (
        np.exp(coefficients.loc[shared_row, "coefficient_log_scale"]) - 1
    ) * 100
    coefficients.to_csv(OUTPUT / "startup_office_seed_funding_model_coefficients.csv", index=False)

    print("Model: log(seed funding) ~ shared office + funding-year indicators")
    print(f"n={n}; residual degrees of freedom={n-k}")
    print(coefficients.to_string(index=False))
    print("\nInterpretation: the shared_office coefficient estimates the funding difference between shared and private offices after adjusting for funding year.")


if __name__ == "__main__":
    main()
