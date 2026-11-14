# Audit the master table and create descriptive summary tables.

required <- c("readr", "dplyr")
missing <- required[!vapply(required, requireNamespace, logical(1), quietly = TRUE)]
if (length(missing)) stop(paste("Install packages:", paste(missing, collapse = ", ")))
library(readr)
library(dplyr)

data_dir <- file.path("data", "processed")
df <- read_csv(file.path(data_dir, "startup_office_seed_funding_master.csv"), show_col_types = FALSE)

audit <- tibble(
  row_count = nrow(df),
  duplicate_company_count = sum(duplicated(tolower(df$company))),
  missing_value_count = sum(is.na(df)),
  invalid_funding_count = sum(is.na(df$seed_funding_usd) | df$seed_funding_usd <= 0),
  invalid_year_count = sum(is.na(df$seed_funding_year) | !df$seed_funding_year %in% 2023:2026),
  shared_count = sum(df$office_space_type == "shared", na.rm = TRUE),
  private_count = sum(df$office_space_type == "private", na.rm = TRUE)
)
write_csv(audit, file.path(data_dir, "startup_office_seed_funding_audit_r.csv"))

summary <- df |>
  group_by(office_space_type) |>
  summarise(
    company_count = n(), mean_funding_usd = mean(seed_funding_usd, na.rm = TRUE),
    median_funding_usd = median(seed_funding_usd, na.rm = TRUE),
    minimum_funding_usd = min(seed_funding_usd, na.rm = TRUE),
    maximum_funding_usd = max(seed_funding_usd, na.rm = TRUE),
    standard_deviation_usd = sd(seed_funding_usd, na.rm = TRUE), .groups = "drop"
  )
write_csv(summary, file.path(data_dir, "startup_office_seed_funding_summary_r.csv"))

by_year <- df |>
  group_by(seed_funding_year, office_space_type) |>
  summarise(
    company_count = n(), median_funding_usd = median(seed_funding_usd, na.rm = TRUE),
    mean_funding_usd = mean(seed_funding_usd, na.rm = TRUE), .groups = "drop"
  )
write_csv(by_year, file.path(data_dir, "startup_office_seed_funding_by_year_r.csv"))
print(audit)
print(summary)
