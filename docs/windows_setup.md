# Windows 11 setup

## 1. Place the project

Copy the project folder to:

```text
C:\Users\kevin\Coding Projects\Short Office Space Project
```

Open that folder in VS Code or RStudio. In RStudio, use **Session > Set Working Directory > To Project Directory**.

## 2. Python environment

Open PowerShell in the project directory:

```powershell
py -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
pip install pandas numpy scipy matplotlib pyyaml
```

If PowerShell blocks activation, run this once, then retry activation:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Run the analysis scripts from the project directory, for example:

```powershell
python scripts\\build_master_dataset.py
python scripts\\analyze_startup_office_seed_funding.py
python scripts\\model_startup_office_seed_funding.py
python scripts\\model_founder_experience.py
python scripts\\model_office_founder_interaction.py
python scripts\\robust_funding_analysis.py
python scripts\\cross_group_analysis.py
python scripts\\create_visualizations.py
```

## 3. R environment

In RStudio, run once:

```r
install.packages(c("readr", "dplyr", "ggplot2", "scales"))
```

Then run the full pipeline from the project root:

```r
source("R/run_all.R")
```

Generated tables appear in `data/processed`; figures appear in `outputs/figures`.

## 4. GitHub

From PowerShell:

```powershell
git init
git add .
git commit -m "Initial office space funding study"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```
