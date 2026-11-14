# Office Space, Founder Experience, and Seed Funding in Bay Area Startups

## Executive summary

This project was an exploratory study on a random sample of 50 Bay Area based startups on whether seed funding differed between Bay Area startups using shared or private office spaces, as well as founder experience.

In this sample, private-office companies overall had higher funding than shared-office companies on both the mean and median measures. Mean seed funding was $8.32 million for private-office companies and $3.08 million for shared-office companies, and median funding was $5.30 million and $2.40 million, respectively. A log-funding regression adjusted for funding year estimated that shared-office companies raised approximately 66.7% less than private-office companies, with p = 0.0166. For example, if a comparable private-office company was predicted to raise $6 million, the model would predict roughly $2 million for the shared-office company.

The founder-experience variable showed little relationship with funding (interesting). The office-space difference remained visible in the four-group comparison, but the interaction between office type and founder experience was not statistically significant. These results merely indicate an association in this collected sample. There are many other variables that go into seed funding that I did not account for.

## 1. Research question and hypothesis

**Research question:** Among Bay Area startups, is seed funding systematically different for companies using shared office space compared with companies using private office spaces, and does founder experience have an association as well (secondary)?

**Primary hypothesis:** Startups using private office space will have higher seed funding than startups using shared office space.

**Side question:** Is documented prior founder experience associated with seed funding, and does it change the relationship between office type and funding?

## 2. Data and measurement

The final master dataset contains 50 startups with publicly documented information about office location, office type, seed funding, funding year, and founders. This data was scraped, audited, and verified from public domain using Python scripts and AI, as well as some manual review.

| Variable | Operational definition |
|---|---|
| Office type | `private` if the company had their own office and `shared` if it operated from a shared-workspace environment |
| Seed funding | Amount (USD) reported for the identified seed round |
| Funding year | Year associated with the identified seed round (2023-2026) |
| Prior founder experience | `1` if one or more founders had documented evidence of previously founding a startup, `0` if no documented evidence was found |

## 3. Sample Summary

| Office type | Companies | Share of sample | Mean funding | Median funding |
|---|---:|---:|---:|---:|
| Private | 35 | 70% | $8.32M | $5.30M |
| Shared | 15 | 30% | $3.08M | $2.40M |
| **Total** | **50** | **100%** | **$6.81M** | **$3.50M** |

For founder experience, in total we had 26 companies with a  `1` and 24 with a `0`.

| Founder experience | Companies | Mean funding | Median funding |
|---|---:|---:|---:|
| Prior founder experience | 26 | $6.49M | $5.15M |
| No documented prior experience | 24 | $7.02M | $3.50M |

The mean funding was slightly higher for companies without documented prior founder experience, while the median funding was higher for companies with prior experience. Interesting, but probably not very statistically significant.

## 4. Findings

Private-office companies raised approximately 2.7 times as much as shared-office companies on the mean measure and approximately 2.2 times as much on the median measure. In this sample, and probably more generally, the mean difference is influenced by very large seed funding rounds, so median is probably a more accurate measure here.

| Comparison | Private / prior experience | Private / no documented experience | Shared / no documented experience | Shared / prior experience |
|---|---:|---:|---:|---:|
| Companies | 17 | 18 | 6 | 9 |
| Mean funding | $8.40M | $8.24M | $3.34M | $2.90M |
| Median funding | $6.00M | $3.50M | $2.70M | $2.00M |

Within private offices, the median difference between companies with and without documented founder experience was modest relative to the office-type difference. Within shared offices, the prior-experience group had a slightly lower median, although the shared/no-experience group was small. I cannot confidently say that there is any clear association between all 3 variables.

## 5. Modelling Results

The primary model estimated log seed funding as a function of office type and funding-year indicators, using private office and 2023 as reference categories just for fun. The interaction model added founder experience and the office-type-by-founder-experience interaction. The only real correlation we have here would be shared vs. private office spaces with funding raised.

| Term | Estimated percentage difference | p-value | Interpretation |
|---|---:|---:|---|
| Shared office | -66.7% | 0.0166 | Shared-office companies had lower predicted funding than private-office companies at the reference founder-experience level |
| Prior founder experience | -1.0% | 0.9744 | No detectable independent funding difference in this sample |
| Shared office × prior experience | +23.4% | 0.7205 | No evidence that founder experience meaningfully changed the office-type relationship |
| 2024 vs. 2023 | -17.3% | 0.7304 | Just for fun |
| 2025 vs. 2023 | +28.9% | 0.6332 | Just for fun |
| 2026 vs. 2023 | +142.6% | 0.0940 | Just for fun |

For founders without documented prior experience, the estimated shared-office difference was approximately -66.7%. For founders with documented prior experience, combining the shared-office and interaction coefficients gives an estimated difference of approximately -58.9%. The interaction p-value indicates that these two estimates should not be treated as meaningfully different based on this sample. There are some figures in the `outputs` folder, feel free to take a look at them!

## 6. Modelling Verification

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

Our findings are consistent with the primary hypothesis as private-office startups raised more seed funding than shared-office startups in this sample. The result is visible in pretty much all of the modelling. For our side question, we didn't find any meaningful relationship between founder experience and seed funding raised. One way to look at this is that not having experience shouldn't deter anyone from striving to be a founder, chase your dreams!

Back to the main question. The analysis cannot establish that private offices cause startups to raise more money. A likely alternative explanation is that companies that already have stronger financing, larger teams, different industries, or more established operations may be more likely to use private offices. The office type may therefore be a marker of company resources rather than the cause of the funding outcome (definitely most likely).

## 8. Limitations

1. The sample is observational.
2. The 50 companies were collected from publicly available sources and may not represent all Bay Area startups.
3. Funding amounts and round labels may differ in reporting quality across sources.
4. Founder experience is based on documented evidence and may undercount experience that was not publicly visible.
5. The shared-office group is smaller than the private-office group.
6. Funding years span 2023-2026, so market conditions may differ across observations. This was for the sake of finding a large enough random sample to study.

## 9. Reproducibility

The project includes Python and R workflows. The files are in the repository. For the scripts in R, run:

```r
source("R/run_all.R")
```

The master data, source/audit fields, scripts, model outputs, and figures are stored in the project folders. The study should be described as an exploratory observational analysis.
