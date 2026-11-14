# Build the analysis-ready master table.
# Run from the project root: source("R/01_prepare_master.R")

required <- c("readr", "dplyr")
missing <- required[!vapply(required, requireNamespace, logical(1), quietly = TRUE)]
if (length(missing)) stop(paste("Install packages:", paste(missing, collapse = ", ")))
library(readr)
library(dplyr)

data_dir <- file.path("data", "processed")
base <- read_csv(file.path(data_dir, "startup_office_seed_funding.csv"), show_col_types = FALSE)
founder <- read_csv(file.path(data_dir, "founder_experience_enrichment.csv"), show_col_types = FALSE)

master <- base |>
  left_join(founder, by = "company", relationship = "one-to-one") |>
  mutate(
    seed_funding_usd = as.numeric(seed_funding_usd),
    seed_funding_year = as.integer(seed_funding_year),
    prior_founder_experience = as.integer(founder_prior_startup_experience),
    shared_office = as.integer(office_space_type == "shared"),
    private_office = as.integer(office_space_type == "private"),
    log_seed_funding = log(seed_funding_usd)
  ) |>
  select(
    company, city, office_address, office_space_type, shared_office, private_office,
    office_evidence_status, seed_funding_usd, seed_funding_year, funding_round_label,
    log_seed_funding, funding_evidence_status, founder_names, prior_founder_experience,
    prior_startup_names, founder_experience_notes, evidence_status, source_urls,
    founder_experience_sources, evidence_notes
  ) |>
  arrange(company)

write_csv(master, file.path(data_dir, "startup_office_seed_funding_master.csv"))
cat("Wrote", nrow(master), "rows to startup_office_seed_funding_master.csv\n")
