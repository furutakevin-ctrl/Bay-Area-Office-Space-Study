# Run from project root with: Rscript R/visualize_funding.R
required <- c("readr", "dplyr", "ggplot2", "scales")
missing <- required[!vapply(required, requireNamespace, logical(1), quietly = TRUE)]
if (length(missing) > 0) stop(paste("Install packages:", paste(missing, collapse = ", ")))
library(readr)
library(dplyr)
library(ggplot2)
library(scales)

df <- read_csv("data/processed/startup_office_seed_funding_master.csv", show_col_types = FALSE)
df <- df |>
  mutate(
    office_space_type = factor(office_space_type, levels = c("private", "shared")),
    founder_experience = if_else(prior_founder_experience == 1, "Prior founder experience", "No documented prior experience"),
    office_founder_group = paste(office_space_type, founder_experience, sep = " / ")
  )
dir.create("outputs/figures", recursive = TRUE, showWarnings = FALSE)

p1 <- ggplot(df, aes(office_space_type, seed_funding_usd, fill = office_space_type)) +
  geom_boxplot(outlier.shape = NA, alpha = .7) + geom_jitter(width = .08, alpha = .65) +
  scale_y_log10(labels = dollar_format()) + scale_fill_manual(values = c(private = "#2C7FB8", shared = "#F28E2B")) +
  labs(title = "Seed funding by office-space type", subtitle = "Log-scaled funding; points are individual companies", x = "Office type", y = "Seed funding (USD)") +
  theme_minimal() + theme(legend.position = "none")
ggsave("outputs/figures/funding_by_office_type.png", p1, width = 8, height = 5, dpi = 300)

p2 <- ggplot(df, aes(founder_experience, seed_funding_usd, fill = founder_experience)) +
  geom_boxplot(outlier.shape = NA, alpha = .7) + geom_jitter(width = .08, alpha = .65) +
  scale_y_log10(labels = dollar_format()) + scale_fill_manual(values = c("Prior founder experience" = "#59A14F", "No documented prior experience" = "#B07AA1")) +
  labs(title = "Seed funding by prior founder experience", subtitle = "Log-scaled funding; points are individual companies", x = "Founder experience", y = "Seed funding (USD)") +
  theme_minimal() + theme(legend.position = "none")
ggsave("outputs/figures/funding_by_founder_experience.png", p2, width = 8, height = 5, dpi = 300)

group_medians <- df |>
  group_by(office_founder_group) |>
  summarise(median_funding = median(seed_funding_usd), .groups = "drop")
p3 <- ggplot(group_medians, aes(reorder(office_founder_group, median_funding), median_funding, fill = office_founder_group)) +
  geom_col(show.legend = FALSE) + coord_flip() + scale_y_continuous(labels = dollar_format()) +
  labs(title = "Median seed funding across office/founder groups", x = NULL, y = "Median seed funding (USD)") + theme_minimal()
ggsave("outputs/figures/four_group_median_funding.png", p3, width = 9, height = 5, dpi = 300)

year_medians <- df |>
  group_by(seed_funding_year, office_space_type) |>
  summarise(median_funding = median(seed_funding_usd), .groups = "drop")
p4 <- ggplot(year_medians, aes(seed_funding_year, median_funding, color = office_space_type, group = office_space_type)) +
  geom_line(linewidth = 1) + geom_point(size = 3) + scale_y_continuous(labels = dollar_format()) +
  scale_color_manual(values = c(private = "#2C7FB8", shared = "#F28E2B")) +
  labs(title = "Median seed funding by year and office type", x = "Funding year", y = "Median seed funding (USD)", color = "Office type") + theme_minimal()
ggsave("outputs/figures/median_funding_by_year_office.png", p4, width = 8, height = 5, dpi = 300)
message("Created four figures in outputs/figures/")
