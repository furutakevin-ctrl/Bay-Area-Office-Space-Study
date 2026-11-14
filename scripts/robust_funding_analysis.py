from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed"
INPUT = DATA / "startup_office_seed_funding_master.csv"
OUTPUT = DATA / "robust_funding_analysis.csv"


def bootstrap_interval(values: np.ndarray, statistic: str, rng: np.random.Generator) -> tuple[float, float]:
    samples = rng.choice(values, size=(10000, len(values)), replace=True)
    if statistic == "mean":
        estimates = samples.mean(axis=1)
    else:
        estimates = np.median(samples, axis=1)
    return tuple(np.percentile(estimates, [2.5, 97.5]))


def main() -> None:
    df = pd.read_csv(INPUT)
    rng = np.random.default_rng(42)
    rows = []

    for variable, groups in [
        ("office_space_type", ["private", "shared"]),
        ("prior_founder_experience", [0, 1]),
    ]:
        for group in groups:
            values = df.loc[df[variable] == group, "seed_funding_usd"].to_numpy()
            mean_ci = bootstrap_interval(values, "mean", rng)
            median_ci = bootstrap_interval(values, "median", rng)
            label = (
                group
                if variable == "office_space_type"
                else {0: "no_prior_experience", 1: "prior_experience"}[group]
            )
            rows.append(
                {
                    "analysis": "bootstrap_group_summary",
                    "grouping_variable": variable,
                    "group": label,
                    "company_count": len(values),
                    "mean_funding_usd": values.mean(),
                    "mean_ci_low": mean_ci[0],
                    "mean_ci_high": mean_ci[1],
                    "median_funding_usd": np.median(values),
                    "median_ci_low": median_ci[0],
                    "median_ci_high": median_ci[1],
                }
            )

        first = df.loc[df[variable] == groups[0], "seed_funding_usd"].to_numpy()
        second = df.loc[df[variable] == groups[1], "seed_funding_usd"].to_numpy()
        test = mannwhitneyu(first, second, alternative="two-sided")
        rows.append(
            {
                "analysis": "mann_whitney_test",
                "grouping_variable": variable,
                "group": f"{groups[0]}_vs_{groups[1]}",
                "company_count": len(first) + len(second),
                "test_statistic": test.statistic,
                "p_value": test.pvalue,
            }
        )

    for excluded_count in [0, 1, 2, 3]:
        trimmed = df.sort_values("seed_funding_usd", ascending=False).iloc[excluded_count:]
        for group in ["private", "shared"]:
            values = trimmed.loc[trimmed["office_space_type"] == group, "seed_funding_usd"]
            rows.append(
                {
                    "analysis": "outlier_sensitivity",
                    "grouping_variable": "office_space_type",
                    "group": group,
                    "excluded_largest_rounds": excluded_count,
                    "company_count": len(values),
                    "mean_funding_usd": values.mean(),
                    "median_funding_usd": values.median(),
                }
            )

    pd.DataFrame(rows).to_csv(OUTPUT, index=False)
    print(pd.DataFrame(rows).to_string(index=False))


if __name__ == "__main__":
    main()
