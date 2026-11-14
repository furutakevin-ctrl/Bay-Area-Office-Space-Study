# Nonparametric tests and bootstrap intervals for the main comparisons.

required <- c("readr", "dplyr")
missing <- required[!vapply(required, requireNamespace, logical(1), quietly = TRUE)]
if (length(missing)) stop(paste("Install packages:", paste(missing, collapse = ", ")))
library(readr)
library(dplyr)

set.seed(42)
data_dir <- file.path("data", "processed")
df <- read_csv(file.path(data_dir, "startup_office_seed_funding_master.csv"), show_col_types = FALSE)

bootstrap_ci <- function(x, statistic = median, reps = 10000) {
  estimates <- replicate(reps, statistic(sample(x, length(x), replace = TRUE)))
  quantile(estimates, c(.025, .975), names = FALSE)
}

groups <- list(
  office_private = df$seed_funding_usd[df$office_space_type == "private"],
  office_shared = df$seed_funding_usd[df$office_space_type == "shared"],
  founder_no_prior = df$seed_funding_usd[df$prior_founder_experience == 0],
  founder_prior = df$seed_funding_usd[df$prior_founder_experience == 1]
)

rows <- lapply(names(groups), function(label) {
  x <- groups[[label]]
  mean_ci <- bootstrap_ci(x, mean)
  median_ci <- bootstrap_ci(x, median)
  tibble(
    grouping_variable = if_else(grepl("office", label), "office_space_type", "prior_founder_experience"),
    group = label, company_count = length(x), mean_funding_usd = mean(x),
    mean_ci_low = mean_ci[1], mean_ci_high = mean_ci[2], median_funding_usd = median(x),
    median_ci_low = median_ci[1], median_ci_high = median_ci[2]
  )
}) |> bind_rows()

tests <- bind_rows(
  tibble(grouping_variable = "office_space_type", group = "private_vs_shared",
         p_value = wilcox.test(groups$office_private, groups$office_shared)$p.value),
  tibble(grouping_variable = "prior_founder_experience", group = "no_prior_vs_prior",
         p_value = wilcox.test(groups$founder_no_prior, groups$founder_prior)$p.value)
)

write_csv(rows, file.path(data_dir, "robust_group_summaries_r.csv"))
write_csv(tests, file.path(data_dir, "robust_tests_r.csv"))
print(rows)
print(tests)
