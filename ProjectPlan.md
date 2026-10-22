# Project Plan: Air Quality, Socioeconomic Conditions, and Respiratory Health Across U.S. Counties

**Course:** IS 477 — Data Management, Curation & Reproducibility  
**Milestone:** 2 - Project Plan 
**Team repository:** https://github.com/tergelm2/TJSR  

## 1. Overview

This project proposes a reproducible county-level data curation workflow to explore the relationship between air quality, socioeconomic conditions, and estimated respiratory health outcomes in the United States. We will acquire three complementary datasets from original government sources: Environmental Protection Agency (EPA) county-level air quality data, U.S. Census Bureau American Community Survey (ACS) socioeconomic estimates, and Centers for Disease Control and Prevention (CDC) PLACES local health estimates. The intended unit of analysis is a U.S. county, linked using standardized five-character county FIPS identifiers.

We will document acquisition, integrity, quality assessment, cleaning, integration and exploratory analysis, paying particular attention to counties missing EPA monitoring. Deliverables will include a county-level dataset, quality metrics, visualization, data dictionary, metadata, and a reproducible modular workflow. The analytical scope is strictly exploratory, focusing on basic summary statistics, variable correlations, and county-level scatter plots. We will not build complex predictive models or make causal claims. 

## 2. Team and Responsibilities


| Role | Member / GitHub username | Primary responsibility | Evidence of contribution |
|---|---|---|---|
| 1 — EPA source lead | Rex Li/@YalinLisys | Retrieve EPA county AQI data; document provenance and coverage; implement acquisition and EPA-specific cleaning | Source notes, acquisition/cleaning script, commits |
| 2 — ACS & CDC source lead | Tergel Myagmarsaikhan / @tergelm2 | Download official CSV datasets from Census and CDC. Check column names, standardize missing values, and select relevant variables.|Acquisition scripts, field notes, commits |
| 3 — Integration & quality lead | Jashan Takhar/ @jashtakhar | Standardize county FIPS codes to five-digit strings. Merge datasets using Pandas, check for duplicate rows, and document missing or dropped counties. Also, produce the analysis and visualization. | Integration/QA scripts, metrics, commits |
| 4 — Documentation & metadata lead | Samuel Kang / @smukng | Coordinate `ProjectPlan.md`, README, source citations, data dictionary and metadata; draft the timeline and constraints; help test `run_all.py` and organize the final release | Documentation files, metadata, reproducibility checks, commits |


## 3. Research Questions

1. How does county-level air quality measures vary with poverty and household-income indicators?
2. How are median AQI and socioeconomic indicators associated with CDC PLACES estimates of adult asthma and chronic obstructive pulmonary disease (COPD) prevalence among counties with comparable available values for the variables being compared?
3. How does geographic coverage and missingness change when the EPA, ACS, and CDC datasets are standardized and integrated? Which counties are lost or lack one or more measures?



## 4. Proposed Datasets and Integration Design

| Source | Planned dataset and contribution | Proposed acquisition | Candidate join key / caveat |
|---|---|---|---|
| U.S. EPA | 2023 AirData annual county Air Quality Index (AQI) summary, median AQI and days with AQI, one row per reporting county, 993 records listed by EPA | Official EPA AirData download: `annual_aqi_by_county_2023.zip` (CSV) | State and county names mapped to county FIPS using Census lookup. Also, review unmatched names and geographic changes. |
| U.S. Census Bureau | 2023 ACS 5-Year county estimates: population, income, and poverty-related variables | Official Census API (JSON) | State FIPS + county FIPS; ACS figures are estimates with survey uncertainty |
| U.S. CDC | PLACES county-level adult asthma and COPD prevalence estimates, using a documented release | Official CDC PLACES data download/API | LocationID (county FIPS), select age-adjusted estimates and reshape measures into columns |

Official starting points: [EPA AirData](https://aqs.epa.gov/aqsweb/airdata/download_files.html), [2023 ACS 5-Year API](https://www.census.gov/data/developers/data-sets/acs-5year/2023.html), and [CDC PLACES](https://www.cdc.gov/places/).  We will inspect sample extracts, confirm at least 100 records per dataset, validate join keys, and record dataset versions. We will use no Kaggle repackaging. For the Census data, we strictly limit our extract to three variables: Total Population, Median Household Income, and Poverty Rate. We intentionally exclude more granular demographic breakdowns to keep the schema simple and focus.

The key is zero-padded five-character `county_fips`. EPA, ACS and CDC IDs will be standardized. We will validate county-key uniqueness and document how long-form CDC measures are reshaped.  We will document unmatched keys and coverage. 

We will save the datasets in the data/raw/ folder to ensure reproducibility. Before downloading, we will check whether the files already exist. We will also use SHA-256 hashes to verify file integrity and make sure the data remains unchanged.

For ACS data, we will focus on total population, median household income, and poverty rate. For CDC PLACES data, we will select asthma (CASTHMA) and COPD (COPD) using MeasureId and keep only age-adjusted prevalence estimates. We will filter the data before merging to avoid duplicate county records.
## 5. Methods, Quality, Ethics, and Reproducibility

We follow acquisition, preservation, assessment, cleaning, integration, analysis and reuse. Raw files remain unchanged under `data/raw/`; outputs use separate directories. A codebook will describe fields, units, coverage and provenance.

An acquisition script for each source will retrieve data from the original provider when allowed, record source URLs and retrieval dates, and calculate SHA-256 checksums. All of data are collected by federal agency and We will review their redistribution terms, properly cite each agency, and document any relevant restrictions. We will properly cite each agency and will not make any causal claims

**Pre-integration quality assessment** will evaluate all four required dimensions for each input: *accuracy* (valid ranges, units, geographic codes, documented provider methods), *completeness* (missing values and geographic coverage), *timeliness* (measurement period, release year, and retrieval date), and *consistency* (type, units, naming, key formats, duplication, and within-dataset contradictions). Issues will be logged with corrective actions. We will distinguish unmonitored observations from zero measurements.

Scripts will normalize types and FIPS codes, handle missing values, and resolve duplicate county-measure rows before joining on `county_fips`. **Post-integration assessment** will repeat the four quality dimensions and report record retention, source coverage, key uniqueness, missingness, temporal compatibility, and plausibility of the integrated fields. Unexpected join multiplication will be diagnosed.

Analysis will provide summaries and at least one visualization, with coverage and model limitations disclosed. Separate scripts for each stage will be orchestrated by `run_all.py` or a `Snakefile`. Relative paths, `requirements.txt` with versions, a full reproduction procedure, a data dictionary, and Schema.org/DCAT/DataCite-style machine-readable metadata will support a clean-clone rerun. Oversized or restricted inputs will follow the course Box requirements.

## 6. Draft Timeline and Deliverables

*Dates below are sequencing targets; replace them with confirmed Canvas dates. Responsible members refer to the provisional role table.*

| Phase / target | Task and output | Lead / support |
|---|---|---|
| Before plan release | Team reviews topic, verifies source access and sample keys, fills names, confirms scope and deadline; revise and commit `ProjectPlan.md` | All; Role 4 coordinates |
| Early implementation | Acquire three source extracts; citations, licenses, retrieval log and SHA-256 manifest | Roles 1 & 2; Role 4 documents |
| Before interim status report (November 19) | Profile each input on accuracy, completeness, timeliness and consistency; document issues and cleaning rules | Roles 1–3 |
| Mid-project | Implement and verify separate cleaning scripts, common schema and county-key integration | Role 3; Roles 1 & 2 |
| After integration | Reassess all four quality dimensions, quantify match rates/unmatched counties and review limitations | Role 3; all review |
| Before final release (December 8)| Add limited analysis/visualization, data dictionary, metadata, `requirements.txt`, full README, and modular orchestrator | Role 4 coordinates documentation; all implement/test |
| Final verification | Fresh-clone end-to-end run, review citations/licenses and contribution history; make final release | All |

## 7. Constraints and Risks

- **Unequal geographic coverage:** EPA monitoring does not cover every county. We will report join coverage and avoid treating absent readings as zero or drawing nationally representative conclusions from monitored counties alone.
- **Temporal comparability:** EPA AQI, ACS 5-Year estimates, and CDC PLACES measures may have different reference periods. We will inspect provider documentation, preserve vintage fields, and interpret temporal mismatches cautiously.
- **Identifier and grain mismatch:** Geographic codes may require padding; CDC records may be long-form by measure. We will test uniqueness and cardinality and avoid many-to-many joins caused by unexamined duplicates.
- **Estimation and measurement limitations:** ACS has survey uncertainty; PLACES provides modeled prevalence; EPA monitors reflect available measurements. We will state these caveats and avoid causal language.

## 8. Gaps

Before the plan release, all members will confirm roles and source versions. Samuel will confirm Canvas
deadlines and the Module 1 lifecycle model. By next week, Rex and Tergel will verify source access, schemas,
record counts and reuse terms. Jashan will test county matches and report unresolved geographic differences. Any required changes will be documented in the status report.

## Preliminary Sources

- U.S. Environmental Protection Agency. *AirData: Download Data Files*. https://aqs.epa.gov/aqsweb/airdata/download_files.html
- U.S. Census Bureau. *2023 ACS 5-Year Data via API*. https://www.census.gov/data/developers/data-sets/acs-5year/2023.html
- Centers for Disease Control and Prevention. *PLACES: Local Data for Better Health*. https://www.cdc.gov/places/
- IS 477. *Course Project Overview & Instructions* (updated September 16, 2026), course-provided document.
