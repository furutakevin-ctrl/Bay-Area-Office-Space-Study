from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed"
INPUT = DATA / "startup_office_seed_funding_master.csv"
OUTPUT = DATA / "office_founder_interaction_model_coefficients.csv"


def main() -> None:
    df = pd.read_csv(INPUT)
    df["log_seed_funding"] = np.log(df["seed_funding_usd"])
    df["shared_office"] = (df["office_space_type"] == "shared").astype(int)
    df["founder_experience"] = df["prior_founder_experience"].astype(int)
    df["office_founder_interaction"] = df["shared_office"] * df["founder_experience"]

    X = pd.DataFrame(
        {
            "intercept": 1.0,
            "shared_office": df["shared_office"],
            "founder_experience": df["founder_experience"],
            "office_founder_interaction": df["office_founder_interaction"],
            "year_2024": (df["seed_funding_year"] == 2024).astype(int),
            "year_2025": (df["seed_funding_year"] == 2025).astype(int),
            "year_2026": (df["seed_funding_year"] == 2026).astype(int),
        }
    )
    y = df["log_seed_funding"].to_numpy()
    x = X.to_numpy()
    beta, _, _, _ = np.linalg.lstsq(x, y, rcond=None)
    residuals = y - x @ beta
    n, k = x.shape
    covariance = (residuals @ residuals) / (n - k) * np.linalg.inv(x.T @ x)
    se = np.sqrt(np.diag(covariance))
    t_values = beta / se
    p_values = 2 * stats.t.sf(np.abs(t_values), df=n - k)
    critical = stats.t.ppf(0.975, df=n - k)

    coefficients = pd.DataFrame(
        {
            "term": X.columns,
            "coefficient_log_scale": beta,
            "standard_error": se,
            "t_statistic": t_values,
            "p_value": p_values,
            "ci_low": beta - critical * se,
            "ci_high": beta + critical * se,
            "percent_change": (np.exp(beta) - 1) * 100,
        }
    )
    coefficients.to_csv(OUTPUT, index=False)

    # Predicted funding for the four office/founder combinations at each year.
    prediction_rows = []
    for office in [0, 1]:
        for founder in [0, 1]:
            for year in [2023, 2024, 2025, 2026]:
                row = np.array(
                    [
                        1,
                        office,
                        founder,
                        office * founder,
                        int(year == 2024),
                        int(year == 2025),
                        int(year == 2026),
                    ],
                    dtype=float,
                )
                prediction_rows.append(
                    {
                        "office_space_type": "shared" if office else "private",
                        "prior_founder_experience": founder,
                        "funding_year": year,
                        "predicted_funding_usd": np.exp(row @ beta),
                    }
                )
    pd.DataFrame(prediction_rows).to_csv(DATA / "office_founder_interaction_predictions.csv", index=False)

    print("Model: log(seed funding) ~ shared office * founder experience + funding year")
    print(f"n={n}; residual degrees of freedom={n-k}")
    print("\nCOEFFICIENTS")
    print(coefficients.to_string(index=False))
    print("\nPREDICTED FUNDING BY GROUP AND YEAR")
    print(pd.DataFrame(prediction_rows).to_string(index=False))


if __name__ == "__main__":
    main()
