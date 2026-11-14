# Office Space and Seed Funding Among Bay Area Startups

## Mini research report

### Executive summary

This project examined whether seed funding differed between Bay Area startups using private office space and startups using shared office space. The final analysis included 50 startups, of which 35 were classified as private-office companies and 15 as shared-office companies. The dataset also recorded whether at least one founder had documented prior startup-founder experience.

In this sample, private-office companies had higher funding than shared-office companies on both the mean and median measures. Mean seed funding was $8.32 million for private-office companies and $3.08 million for shared-office companies. Median funding was $5.30 million and $2.40 million, respectively. A log-funding regression adjusted for funding year estimated that shared-office companies raised approximately 66.7% less than private-office companies, with p = 0.0166.

The founder-experience variable showed little relationship with funding. The office-space difference remained visible in the four-group comparison, but the interaction between office type and founder experience was not statistically significant. These results indicate an association in this collected sample, not a causal effect of office type. Company age, industry, founder quality, investor networks, geography, and selection into office type may explain part or all of the observed difference.

## 1. Research question and hypothesis

**Research question:** Among Bay Area startups, is seed funding systematically different for companies using shared office space compared with companies using private office space?

**Primary hypothesis:** Startups using private office space will have higher seed funding than startups using shared office space.

**Secondary question:** Is documented prior founder experience associated with seed funding, and does it change the relationship between office type and funding?

## 2. Data and measurement

The final master dataset contains 50 startups with publicly documented information about office location, office type, seed funding, funding year, and founders.

| Variable | Operational definition |
|---|---|
| Office type | `private` if the company appeared to operate from its own office; `shared` if it operated from a coworking or shared-workspace environment |
| Seed funding | Amount reported for the identified seed round, in U.S. dollars |
| Funding year | Year associated with the identified seed round; observations span 2023-2026 |
| Prior founder experience | `1` if at least one founder had documented evidence of previously founding a startup; `0` if no documented evidence was found |

The founder variable should be interpreted carefully: a value of `0` means no documented evidence was found in the reviewed sources, not proof that no founder had ever started a company.

## 3. Sample composition

| Office type | Companies | Share of sample | Mean funding | Median funding |
|---|---:|---:|---:|---:|
| Private | 35 | 70% | $8.32M | $5.30M |
| Shared | 15 | 30% | $3.08M | $2.40M |
| **Total** | **50** | **100%** | **$6.81M** | **$3.50M** |

Founder experience was coded as documented prior experience for 26 companies and no documented prior experience for 24 companies.

## 4. Descriptive findings

Private-office companies raised approximately 2.7 times as much as shared-office companies on the mean measure and approximately 2.2 times as much on the median measure. The mean difference is influenced by several large private-office funding rounds, so the median is also reported as a more robust comparison.

| Comparison | Private / prior experience | Private / no documented experience | Shared / no documented experience | Shared / prior experience |
|---|---:|---:|---:|---:|
| Companies | 17 | 18 | 6 | 9 |
| Mean funding | $8.40M | $8.24M | $3.34M | $2.90M |
| Median funding | $6.00M | $3.50M | $2.70M | $2.00M |

Within private offices, the median difference between companies with and without documented founder experience was modest relative to the office-type difference. Within shared offices, the prior-experience group had a slightly lower median, although the shared/no-experience group was small.

## 5. Regression results

The primary model estimated log seed funding as a function of office type and funding-year indicators, using private office and 2023 as reference categories. The interaction model added founder experience and the office-type-by-founder-experience interaction.

| Term | Estimated percentage difference | p-value | Interpretation |
|---|---:|---:|---|
| Shared office | -66.7% | 0.0166 | Shared-office companies had lower predicted funding than private-office companies at the reference founder-experience level |
| Prior founder experience | -1.0% | 0.9744 | No detectable independent funding difference in this sample |
| Shared office × prior experience | +23.4% | 0.7205 | No evidence that founder experience meaningfully changed the office-type relationship |
| 2024 vs. 2023 | -17.3% | 0.7304 | Not statistically significant |
| 2025 vs. 2023 | +28.9% | 0.6332 | Not statistically significant |
| 2026 vs. 2023 | +142.6% | 0.0940 | Suggestive but imprecise; likely affected by small year-specific counts |

For founders without documented prior experience, the estimated shared-office difference was approximately -66.7%. For founders with documented prior experience, combining the shared-office and interaction coefficients gives an estimated difference of approximately -58.9%. The interaction p-value indicates that these two estimates should not be treated as meaningfully different based on this sample.

## 6. Robustness checks

Because funding amounts are skewed, the analysis included medians, bootstrap intervals, and a Mann-Whitney test.

| Test | Result |
|---|---:|
| Private vs. shared office, Mann-Whitney p-value | 0.0021 |
| Prior experience vs. no documented experience, Mann-Whitney p-value | 0.8688 |
| Private mean after excluding three largest rounds | $6.22M |
| Shared mean after excluding three largest rounds | $3.08M |
| Private median after excluding three largest rounds | $4.50M |
| Shared median after excluding three largest rounds | $2.40M |

The private-office funding advantage remained after removing the three largest rounds, although the difference became smaller. This supports the conclusion that the descriptive result is not driven entirely by a few extreme observations.

## 7. Interpretation

The collected data are consistent with the primary hypothesis: private-office startups raised more seed funding than shared-office startups in this sample. The result is visible in the raw means, medians, four-group comparison, adjusted regression, and nonparametric test.

However, the analysis cannot establish that private offices cause startups to raise more money. A likely alternative explanation is selection: companies that already have stronger financing, larger teams, different industries, or more established operations may be more likely to use private offices. The office type may therefore be a marker of company resources rather than the cause of the funding outcome.

Founder experience did not show a meaningful independent relationship with seed funding, and there was no reliable evidence that it changed the relationship between office type and funding.

## 8. Limitations

1. The sample is observational and not randomly assigned to office types.
2. The 50 companies were collected from publicly available sources and may not represent all Bay Area startups.
3. Shared versus private office classification can be difficult when companies list only a building or mailing address.
4. Funding amounts and round labels may differ in reporting quality across sources.
5. Founder experience is based on documented evidence and may undercount experience that was not publicly visible.
6. The shared-office group is smaller than the private-office group, and some four-group cells are small.
7. Funding years span 2023-2026, so market conditions may differ across observations.

## 9. Reproducibility

The project includes Python and R workflows. From the project root, the R workflow can be run with:

```r
source("R/run_all.R")
```

The master data, source/audit fields, scripts, model outputs, and figures are stored in the project folders. The study should be described as an exploratory observational analysis rather than a causal estimate.
