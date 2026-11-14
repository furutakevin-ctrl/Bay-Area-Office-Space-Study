# Master dataset data dictionary

File: `startup_office_seed_funding_master.csv`

| Field | Meaning |
|---|---|
| `company` | Company name |
| `city` | Bay Area city |
| `office_address` | Reported office location |
| `office_space_type` | Shared or private office classification |
| `shared_office` | 1 for shared, 0 otherwise |
| `private_office` | 1 for private, 0 otherwise |
| `seed_funding_usd` | Seed-round amount in U.S. dollars |
| `seed_funding_year` | Year of the seed round |
| `funding_round_label` | Round label used in the source evidence |
| `log_seed_funding` | Natural logarithm of seed funding; used for modeling |
| `founder_names` | Founders identified during the enrichment review |
| `prior_founder_experience` | 1 if at least one founder previously founded a startup; 0 if no prior founder evidence was documented |
| `prior_startup_names` | Previously founded startups identified |
| `founder_experience_notes` | Coding rationale |
| `source_urls` | Office and funding sources |
| `founder_experience_sources` | Founder-experience sources |
| `evidence_notes` | Office and funding evidence notes |

The founder-experience indicator is an operational, source-based measure. A value of 0 means no prior startup-founder evidence was documented in the reviewed sources; it does not prove that a founder has never started another company.
