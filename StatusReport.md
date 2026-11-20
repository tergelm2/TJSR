# Milestone 3 — Interim Status Report

**Project:** Air Quality, Socioeconomic Conditions, and Respiratory Health Across U.S. Counties  
**Course:** IS 477 — Data Management, Curation & Reproducibility (Fall 2026)  
**Reporting date:** November 19, 2026  
**Team:** Rex Li (@YalinLisys), Tergel Myagmarsaikhan (@tergelm2), Jashan Takhar (@jashtakhar), Samuel Kang (@smukng)  
**Repository:** [TJSR](https://github.com/tergelm2/TJSR) · **Revised plan:** [ProjectPlan.md](ProjectPlan.md)

## 1. Research scope and interim assessment

Our project studies descriptive county-level associations among air quality, socioeconomic conditions, and modeled adult respiratory-health prevalence. We combine 2023 EPA Annual Air Quality Index (AQI) summaries, the 2019–2023 Census American Community Survey (ACS) five-year estimates, and the December 2025 CDC PLACES county release using five-character county FIPS identifiers. Variables cover AQI, monitoring days, income, poverty, and age-adjusted asthma/COPD prevalence. We will not infer causation or treat absent monitors as zero pollution.

Acquisition, initial source QA, EPA FIPS mapping, and **EPA–CDC integration** are complete. The ACS join and three-source analysis remain unfinished.

## 2. Progress against the Milestone 2 plan

### 2.1 Sources, acquisition, and provenance — complete

**EPA (Rex).** The official 2023 Annual AQI by County archive contains **993 records and 18 columns**. The original archive, download information, and SHA-256 checksum are preserved in [raw data](data/raw/annual_aqi_by_county_2023.zip), [source notes](data/raw/epa_source_notes.md), and [hash.py](hash.py).

**ACS and CDC (Tergel).** ACS Detailed Tables B01003 (population), B19013 (median household income), and B17001 (poverty numerator/denominator) were obtained alongside CDC PLACES asthma (`CASTHMA`) and COPD (`COPD`) age-adjusted estimates. The selected CDC release is `swc5-untb`, based on 2023 BRFSS data. The CDC extract is committed; the three ACS `.dat` inputs are documented but not committed. Acquisition URLs, byte sizes, retrieval date, and checksums appear in [sources.json](data/raw/acs_cdc/sources.json) and [source notes](data/raw/acs_cdc/source_notes.md).

### 2.2 Pre-integration quality assessment — complete for current inputs

Rex's [EPA report](epa_quality.md) and [quality.py](quality.py) assess accuracy, completeness, timeliness, and consistency: **no missing cells, duplicate county pairs, or negative median AQI values** were found. Median AQI ranged from 3 to 77; eight maximum-AQI values exceeded 500 and require careful interpretation rather than automatic deletion. Reporting days ranged from 55 to 365, demonstrating uneven monitoring coverage. Jurisdictional records also required review.

Tergel's [acs_cdc.py](acs_cdc.py) and [source notes](data/raw/acs_cdc/source_notes.md) document **3,222 unique ACS county/county-equivalent identifiers** in each table, with two missing median-income estimates. The CDC extract contains **5,916 records**, including two national summary rows, representing **2,957 counties** across the two measures. Asthma and COPD estimates are suppressed for Loving County, Texas. Missingness is not interpreted as zero.

### 2.3 Cleaning, identifiers, and integration — partly complete

Jashan developed [epa_fips.py](epa_fips.py) to normalize EPA geographic names and assign five-digit FIPS codes. The documented [override table](data/lookup/epa_fips_overrides.csv) corrects seven ambiguous or misspelled names, including independent-city/county collisions. Two out-of-scope jurisdiction rows were excluded; **991 EPA records received unique FIPS codes**. See the [processed EPA file](data/processed/epa_aqi_2023_fips.csv) and [exclusion log](data/processed/epa_unmatched.csv).

The [integration script](integrate.py) reshapes CDC measures into one record per county, verifies unique FIPS codes, and uses validated one-to-one outer joins. Its current EPA–CDC output is [county_integrated.csv](data/processed/county_integrated.csv); [coverage_summary.csv](data/processed/coverage_summary.csv) reports:

| Coverage measure | County count |
|---|---:|
| EPA with standardized FIPS | 991 |
| CDC PLACES | 2,957 |
| Present in both EPA and CDC | **912** |
| EPA only (no CDC match) | 79 |
| CDC only (no EPA AQI) | 2,045 |

All 912 matched counties have values for median AQI, asthma, and COPD. Source-presence flags preserve geographic gaps. The ACS join is coded but skipped without local `.dat` files. Thus, **three-source data, merged QA, and final analysis are incomplete**.

### 2.4 Analysis, documentation, and reproducibility — in progress

Planned outputs include summary statistics, correlations, scatter plots, and coverage summaries. Figures will state sample sizes, missingness, units, and reference periods. None are committed yet. The current [requirements.txt](requirements.txt) pins `pandas` and `addfips`, and source checksums are documented. A comprehensive `README.md`, data dictionary, machine-readable metadata, single-command workflow, and independent fresh-clone verification are **still planned**, not completed.

## 3. Updated task schedule

Dates are working targets.

| Task / artifact | Owner | Status at Nov. 19 | Next target |
|---|---|---|---|
| Project scope, roles, and revised [plan](ProjectPlan.md) | All; Samuel | Complete | Nov. 19 |
| EPA acquisition, provenance, and source QA | Rex | Complete | Nov. 18 |
| ACS/CDC acquisition, source checks, and hashes | Tergel | Complete; large ACS inputs external | Nov. 19 |
| EPA FIPS mapping and [override log](data/lookup/epa_fips_overrides.csv) | Jashan | Complete | Nov. 19 |
| EPA–CDC integration and [coverage report](data/processed/coverage_summary.csv) | Jashan | Complete | Nov. 19 |
| ACS retrieval mechanism and checksum verification | Tergel | Pending | Nov. 24 |
| Three-source join, Connecticut rule, and merged QA | Jashan; Rex supports | Pending | Nov. 29 |
| Metadata inventory and variable/reference-period notes | Samuel | Pending | Dec. 1 |
| Plots, statistics, sensitivity checks, and quality assessment | Jashan; all review | Pending | Dec. 3 |
| Acquisition automation and reproducible entry point | Rex, Tergel, Jashan | Pending | Dec. 3 |
| README, dictionary, metadata, clean-clone test | Samuel; all test | Pending | Dec. 6 |
| Final project release | All | Pending | Dec. 8 |

## 4. Changes after Milestone 2 feedback

Milestone 2 received **19/20**. The grader requested a clearer answer to *which U.S. counties* are studied, a more directed research question, and a concrete account of reproducibility. The revised [ProjectPlan.md](ProjectPlan.md) therefore (1) separates the broad county-coverage inventory from the subset eligible for AQI-based comparisons; (2) focuses on median AQI, income, poverty, asthma, and COPD, with coverage/missingness as an explicit secondary question; and (3) specifies retained raw inputs, source versions and SHA-256 hashes, five-digit FIPS checks, modular scripts, dependency versions, documented execution order, and a future clean-clone test. Implementation remains partial.

## 5. Challenges, decisions, and mitigation

**Uneven EPA coverage and selection bias.** EPA has 991 in-scope county records versus 2,957 CDC counties; 912 overlap. Among those 912, the team identified 162 with fewer than 274 monitored days. **Action:** retain missing source flags, document excluded counties, and compare final results with and without a monitoring-days threshold before drawing conclusions.

**Geographic definitions and temporal mismatch.** Seven EPA names required [manual FIPS overrides](data/lookup/epa_fips_overrides.csv), now documented and applied. Connecticut's eight historical EPA counties do not map one-to-one onto the nine planning regions used by ACS/CDC; the team plans to exclude Connecticut from cross-source AQI analyses while reporting the mismatch. CDC lacks Kentucky and Pennsylvania estimates in this release; Puerto Rico also falls outside its coverage. EPA's 2023 calendar year, ACS's five-year window, and CDC's modeled estimates are not identical observation periods. **Action:** document exclusions and reference periods, and avoid longitudinal or causal claims.

**Large inputs and reproducibility.** ACS poverty file `acsdt5y2023-b17001.dat` is approximately **118 MB**, exceeding GitHub's 100 MB file limit. The source quality script requires local downloads, while integration currently skips absent ACS inputs. **Action:** Tergel will arrange accessible external storage or source retrieval with checksum verification; the team will document download instructions and add an orchestrator. A fresh-clone rerun is a required *future check*, not a demonstrated result.

## 6. Individual contributions

Each member must review and commit **their own summary**; Git history establishes authorship.

- **Rex Li (@YalinLisys):** I acquired the EPA 2023 annual county AQI archive, preserved its checksum and source notes, and wrote the initial quality assessment. I reported missingness, uniqueness, AQI ranges, monitoring coverage, and records needing jurisdictional review. Evidence: [quality report](epa_quality.md), [hash.py](hash.py), [quality.py](quality.py), and [my report commit](https://github.com/tergelm2/TJSR/commit/ef2201d231fba2ef59489bf09fcb12246130c011).
- **Tergel Myagmarsaikhan (@tergelm2):** I acquired and documented the Census ACS and CDC PLACES source extracts, selected the population, income, poverty, asthma and COPD variables, and checked county identifiers, missing estimates, duplicates, and value ranges. Evidence: [source notes](data/raw/acs_cdc/source_notes.md), [acs_cdc.py](acs_cdc.py), and [my commits](https://github.com/tergelm2/TJSR/commits?author=tergelm2).
- **Jashan Takhar (@jashtakhar):** I implemented EPA county FIPS mapping and seven documented overrides, prepared the EPA–CDC county-level integration, added key/merge validation, and produced the coverage and integrated-data files. I identified the Connecticut geography mismatch and missing CDC state coverage and updated the report's technical sections. Evidence: [epa_fips.py](epa_fips.py), [integrate.py](integrate.py), and [my commits](https://github.com/tergelm2/TJSR/commits?author=jashtakhar).
- **Samuel Kang (@smukng):** I coordinated the interim reporting, created the initial `StatusReport.md`, consolidated team updates and artifact links, and revised the project plan in response to the grader's concerns about county scope, research focus, and reproducibility. I will coordinate documentation, metadata, and final release checks. Evidence: [revised plan](ProjectPlan.md) and [my plan revision commit](https://github.com/tergelm2/TJSR/commit/0819f51b32b6276a2c47ec3caa703745a925c03c).

## 7. Milestone submission

All referenced in-progress artifacts should be committed before the milestone snapshot. After the four contribution summaries have been individually reviewed and committed, publish the **`status-report`** tag and GitHub Release from the final branch state, and submit the **Release URL** in Canvas. Outstanding analysis and reproducibility items remain scheduled for Milestone 4.
