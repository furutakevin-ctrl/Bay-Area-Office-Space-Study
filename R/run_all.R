# Run the complete R workflow from the project root.
# In RStudio: setwd("C:/Users/kevin/Coding Projects/Short Office Space Project")
# Then run: source("R/run_all.R")

source(file.path("R", "01_prepare_master.R"))
source(file.path("R", "02_audit_and_summary.R"))
source(file.path("R", "03_models.R"))
source(file.path("R", "04_robust_analysis.R"))
source(file.path("R", "visualize_funding.R"))

cat("Complete R workflow finished.\n")
