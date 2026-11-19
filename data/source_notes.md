# ACS and CDC data notes

We downloaded both sources on November 19, 2026. [Download links, file sizes, and SHA-256 checksums](sources.json)

## American Community Survey

We used three Detailed Tables from the Census Bureau's 2019–2023 ACS five-year Summary File, released on December 12, 2024. For the quality checks, we identified county and county-equivalent records by the `0500000US` prefix in `GEO_ID`. [Census release](https://www.census.gov/programs-surveys/acs/news/data-releases/2023/release.html) · [Original tables](https://www2.census.gov/programs-surveys/acs/summary_file/2023/table-based-SF/data/5YRData/) · [Census citation guidance](https://www.census.gov/about/policies/citation.html)

| ACS field | Definition |
|---|---|
| `B01003_E001` | Estimated total population |
| `B19013_E001` | Median household income in the past 12 months, in 2023 inflation-adjusted dollars |
| `B17001_E001` | Estimated number of people for whom poverty status is determined |
| `B17001_E002` | Estimated number of people with income below the poverty level |

All three tables had the same 3,222 county or county-equivalent FIPS codes, including 78 Puerto Rico municipios. Population and poverty estimates were complete. The Census file marked income estimates as missing for Esmeralda County, Nevada (`32009`), and Kenedy County, Texas (`48261`). Poverty rates ranged from 1.70% to 64.75%, calculated as `100 × B17001_E002 / B17001_E001`. The original tables include margins of error for the survey estimates. [ACS Summary File handbook](https://www.census.gov/content/dam/Census/library/publications/2023/acs/acs_table_based_summary_file_handbook.pdf)

## CDC PLACES

We used the December 2025 CDC PLACES county release (`swc5-untb`). The download asks for asthma (`CASTHMA`) and COPD (`COPD`) with `DataValueTypeID=AgeAdjPrv`. Both are modeled age-adjusted estimates of adult prevalence, reported as percentages and based on 2023 BRFSS data. The repo includes the original download. CDC publishes these public-domain data for free. CDC endorsement is neither claimed nor implied. [Dataset](https://data.cdc.gov/d/swc5-untb) · [Dataset license](https://data.cdc.gov/api/views/swc5-untb.json) · [CDC release notes](https://www.cdc.gov/places/current-release-notes/)

The download had 5,916 rows, including two U.S. summary rows (`LocationID=59`). We left the U.S. rows out of the county checks. The county rows use five-digit FIPS codes and contain one row per county and measure, for 2,957 counties. Asthma ranged from 7.8% to 15.1%, and COPD ranged from 3.2% to 15.0%. Both estimates are blank for Loving County, Texas (`48301`), because CDC suppressed them. CDC did not publish 2023 BRFSS-based estimates for Kentucky or Pennsylvania, and the release covers the 50 states and D.C. [CDC release notes](https://www.cdc.gov/places/current-release-notes/)

## Check the downloads

Download the three Census `.dat` files listed in [sources.json](sources.json) into `data/raw/acs_cdc/`. The CDC download is already in that folder. From the repo root, run `python acs_cdc.py` with Python 3.11 or newer. The script checks the four SHA-256 hashes and prints the source quality results. [Quality check script](../../../acs_cdc.py)
