# Bay Area Startup Office Space Study

This project examines whether seed funding differs between Bay Area startups using shared versus private office space. It also explores whether documented prior founder experience is associated with funding outcomes.

## Current dataset

The master file contains 50 startups with:

- office-space type: `shared` or `private`
- seed funding amount and year
- founder-experience indicator: `1` if at least one founder had a documented prior startup, otherwise `0` for no documented evidence
- source and audit fields for reproducibility

This is an observational study. The results describe associations in the collected sample; they do not establish that office type causes higher or lower funding.

## Final project structure

```text
data/processed/    final cleaned master data and analysis tables
scripts/           Python data preparation, modeling, and preview charts
R/                 reproducible R cleaning, modeling, and visualization scripts
outputs/figures/   generated PNG figures
outputs/pdf/       final PDF report
docs/              Windows setup instructions
report/            editable Markdown report
```

This repository is intentionally limited to the final Bay Area startup scope. Earlier geography screens, SF-only samples, YC screens, SEC/DataSF discovery files, and exploratory collection scripts were excluded from this final version.

## Reproduce the analysis

From this `project` directory:

```bash
python scripts/analyze_startup_office_seed_funding.py
python scripts/model_startup_office_seed_funding.py
python scripts/model_founder_experience.py
python scripts/model_office_founder_interaction.py
python scripts/robust_funding_analysis.py
python scripts/cross_group_analysis.py
python scripts/create_visualizations.py
```

For the full R workflow, install the packages once and run:

```r
install.packages(c("readr", "dplyr", "ggplot2", "scales"))
```

Then, from the project directory:

```bash
Rscript R/run_all.R
```

The individual R stages are also available:

```text
R/01_prepare_master.R       Build the analysis-ready master table
R/02_audit_and_summary.R    Audit data and create descriptive tables
R/03_models.R               Fit office, founder, year, and interaction models
R/04_robust_analysis.R      Run bootstrap summaries and Wilcoxon tests
R/visualize_funding.R       Create the four figures
R/run_all.R                 Run all stages in order
```

## Main research question

Among the startups in this collected sample, is seed funding systematically different for companies using shared office space compared with companies using private office space, after accounting for funding year and documented founder experience?
