# Fit the main log-funding models and export coefficients/predictions.

required <- c("readr", "dplyr")
missing <- required[!vapply(required, requireNamespace, logical(1), quietly = TRUE)]
if (length(missing)) stop(paste("Install packages:", paste(missing, collapse = ", ")))
library(readr)
library(dplyr)

data_dir <- file.path("data", "processed")
df <- read_csv(file.path(data_dir, "startup_office_seed_funding_master.csv"), show_col_types = FALSE) |>
  mutate(
    office_space_type = factor(office_space_type, levels = c("private", "shared")),
    prior_founder_experience = as.integer(prior_founder_experience),
    seed_funding_year = factor(seed_funding_year, levels = 2023:2026),
    shared_office = as.integer(office_space_type == "shared"),
    log_seed_funding = log(seed_funding_usd)
  )

export_model <- function(model, name) {
  co <- as.data.frame(summary(model)$coefficients)
  names(co) <- c("estimate", "standard_error", "t_statistic", "p_value")
  ci <- as.data.frame(confint(model))
  names(ci) <- c("ci_low", "ci_high")
  out <- cbind(term = rownames(co), co, ci)
  out <- as_tibble(out) |>
    mutate(across(-term, as.numeric), percent_difference = (exp(estimate) - 1) * 100,
           model = name) |>
    select(model, everything())
  write_csv(out, file.path(data_dir, paste0(name, "_coefficients_r.csv")))
  invisible(model)
}

m_office <- lm(log_seed_funding ~ shared_office + seed_funding_year, data = df)
m_founder <- lm(log_seed_funding ~ prior_founder_experience + seed_funding_year, data = df)
m_interaction <- lm(log_seed_funding ~ shared_office * prior_founder_experience + seed_funding_year, data = df)

export_model(m_office, "office_year_model")
export_model(m_founder, "founder_year_model")
export_model(m_interaction, "office_founder_interaction_model")

prediction_grid <- expand.grid(
  shared_office = 0:1,
  prior_founder_experience = 0:1,
  seed_funding_year = factor(2023:2026, levels = 2023:2026)
) 
prediction_grid$predicted_funding_usd <- exp(predict(m_interaction, newdata = prediction_grid))
prediction_grid <- prediction_grid |>
  mutate(office_space_type = if_else(shared_office == 1, "shared", "private"))
write_csv(prediction_grid, file.path(data_dir, "office_founder_interaction_predictions_r.csv"))

cat("Models completed.\n")
print(summary(m_interaction))
