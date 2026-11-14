"""Create preview figures for the seed-funding analysis.

Run from the project directory with: python scripts/create_visualizations.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "startup_office_seed_funding_master.csv"
OUT = ROOT / "outputs" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA)
df["founder_experience_label"] = np.where(
    df["prior_founder_experience"].eq(1),
    "Prior founder experience",
    "No documented prior experience",
)

COLORS = {"private": "#2C7FB8", "shared": "#F28E2B"}
plt.rcParams.update({"figure.dpi": 130, "axes.spines.top": False, "axes.spines.right": False})


def money(x, _):
    return f"${x / 1_000_000:.1f}M" if x >= 1_000_000 else f"${x / 1_000:.0f}K"


def boxplot(column, labels, filename, title, colors):
    groups = [df.loc[df[column].eq(label), "seed_funding_usd"].dropna().values for label in labels]
    fig, ax = plt.subplots(figsize=(8, 5))
    bp = ax.boxplot(groups, labels=labels, patch_artist=True, showfliers=False)
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.65)
    rng = np.random.default_rng(42)
    for i, values in enumerate(groups, 1):
        ax.scatter(i + rng.uniform(-0.08, 0.08, len(values)), values, s=24, alpha=.65, color=colors[i - 1])
    ax.set_yscale("log")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(money))
    ax.set_ylabel("Seed funding (USD)")
    ax.set_title(title)
    ax.grid(axis="y", alpha=.25)
    fig.tight_layout()
    fig.savefig(OUT / filename, dpi=300)
    plt.close(fig)


boxplot(
    "office_space_type", ["private", "shared"], "funding_by_office_type.png",
    "Seed funding by office-space type", [COLORS["private"], COLORS["shared"]],
)
boxplot(
    "founder_experience_label",
    ["Prior founder experience", "No documented prior experience"],
    "funding_by_founder_experience.png",
    "Seed funding by prior founder experience",
    ["#59A14F", "#B07AA1"],
)

groups = df.groupby(["office_space_type", "founder_experience_label"], sort=False)["seed_funding_usd"].median().sort_values()
fig, ax = plt.subplots(figsize=(9, 5))
labels = [f"{office} / {experience}" for (office, experience) in groups.index]
ax.barh(labels, groups.values, color=[COLORS[o] for o, _ in groups.index])
ax.xaxis.set_major_formatter(plt.FuncFormatter(money))
ax.set_xlabel("Median seed funding (USD)")
ax.set_title("Median seed funding across office/founder groups")
ax.grid(axis="x", alpha=.25)
fig.tight_layout()
fig.savefig(OUT / "four_group_median_funding.png", dpi=300)
plt.close(fig)

year = df.groupby(["seed_funding_year", "office_space_type"])["seed_funding_usd"].median().reset_index()
fig, ax = plt.subplots(figsize=(8, 5))
for office, sub in year.groupby("office_space_type"):
    ax.plot(sub["seed_funding_year"], sub["seed_funding_usd"], marker="o", linewidth=2, label=office, color=COLORS[office])
ax.yaxis.set_major_formatter(plt.FuncFormatter(money))
ax.set_xlabel("Funding year")
ax.set_ylabel("Median seed funding (USD)")
ax.set_title("Median seed funding by year and office type")
ax.legend(title="Office type")
ax.grid(alpha=.25)
fig.tight_layout()
fig.savefig(OUT / "median_funding_by_year_office.png", dpi=300)
plt.close(fig)

print(f"Created four figures in {OUT}")
