[ProjectPlan (1).md](https://github.com/user-attachments/files/34948857/ProjectPlan.1.md)

# Project Plan: Air Quality, Socioeconomic Conditions, and Respiratory Health Across U.S. Counties

**Course:** IS 477 — Data Management, Curation & Reproducibility  
**Milestone:** 2 — Project Plan (revised for Milestone 3)  
**Team repository:** https://github.com/tergelm2/TJSR  
**Revision date:** November 16, 2026  

## 1. Overview and Refined Scope

This project proposes a reproducible, county-level data curation workflow to investigate exploratory associations among air quality, socioeconomic conditions, and estimated respiratory-health outcomes. We plan to acquire data from three original federal sources: the U.S. Environmental Protection Agency (EPA) AirData county-level Air Quality Index (AQI) summaries, U.S. Census Bureau American Community Survey (ACS) estimates, and Centers for Disease Control and Prevention (CDC) PLACES county health estimates. Each integrated observation will represent one U.S. county identified by a zero-padded five-character `county_fips` code.

**Geographic scope and selection rule (clarified after Milestone 2 feedback):** The study is intended to cover U.S. counties represented in the county-level ACS/CDC source data, with EPA AQI availability determined separately. We will first build and describe the overall county coverage of the three datasets. For analyses using AQI, the eligible analytical sample will include only counties having valid, comparable EPA AQI values and the relevant ACS/CDC variables. Counties missing EPA monitoring will not receive an invented AQI value or be treated as having zero pollution; they will be reported in the coverage/missingness assessment. We will publish counts and a list of included and excluded FIPS codes, plus the reason for each exclusion. We will verify the precise geographic scope (including county equivalents and territories) against the downloaded releases instead of assuming that every U.S. county is represented.

The primary outputs will be documented raw-source snapshots or acquisition instructions, a cleaned/integrated county-level dataset, pre- and post-integration quality assessments, an inclusion/exclusion report, basic descriptive statistics and visualizations, a data dictionary, metadata, and an executable workflow. The purpose is data integration and curation, not prediction or causal inference.

## 2. Team and Responsibilities

| Role | Member / GitHub username | Primary responsibility | Evidence of contribution |
|---|---|---|---|
| 1 — EPA source lead | Rex Li / @YalinLisys | Retrieve EPA county AQI data, document provenance and coverage, and implement acquisition/EPA-specific cleaning | Source notes, scripts, quality results, commits |
| 2 — ACS & CDC source lead | Tergel Myagmarsaikhan / @tergelm2 | Acquire official ACS/CDC data; check fields, types and missingness; select relevant variables | Acquisition/cleaning scripts, notes, commits |
| 3 — Integration & quality lead | Jashan Takhar / @jashtakhar | Normalize county FIPS, integrate sources, test join cardinality, summarize coverage and generate exploratory outputs | Integration/QA scripts, match reports, charts, commits |
| 4 — Documentation & metadata lead | Samuel Kang / @smukng | Maintain plan, status report, source citations, data dictionary, metadata, README, reproducibility checklist and release documentation | Documentation, metadata, validation notes, commits |

Tasks and ownership are proposed allocations from the original plan; the status report will record actual completed work and changes confirmed by each member. Each member will write and commit their own Milestone 3 contribution summary.

## 3. Refined Research Questions

**Primary question:** Among U.S. counties with available, comparable observations, how are 2023 county-level median AQI, median household income and poverty rate associated with CDC PLACES estimates of adult asthma and COPD prevalence?

Supporting questions:

1. How do median AQI and observed air-quality coverage vary across counties with different ACS median household incomes and poverty rates?
2. Among counties with valid matched values, what are the descriptive associations of median AQI and socioeconomic indicators with adult asthma and COPD prevalence estimates? We will present these as descriptive comparisons and correlations only, not causal effects.
3. How many counties are represented in each original dataset, how many match by `county_fips`, and which counties or attributes are missing after integration? How do inclusion rules affect the resulting sample?

These questions narrow the analysis to specified variables, an explicit county-level unit, and clear eligibility criteria. Potential temporal mismatch between 2023 EPA/ACS observations and the selected CDC PLACES release will be documented; results will not be framed as perfectly synchronized longitudinal observations.

## 4. Sources, Variables, and County Integration

| Source | Planned data and variables | Acquisition and provenance | Geographic key and special handling |
|---|---|---|---|
| EPA AirData | 2023 `annual_aqi_by_county_2023.zip`: county-level AQI summary, especially median AQI and monitoring-day/coverage information | [EPA AirData official download](https://aqs.epa.gov/aqsweb/airdata/download_files.html); retain URL, retrieval date, original filename and SHA-256 checksum | EPA state/county names require a documented crosswalk to county FIPS; validate ambiguous/unmatched names |
| Census ACS | 2023 ACS 5-Year county estimates: total population, median household income and poverty rate | [Census ACS 5-Year API documentation](https://www.census.gov/data/developers/data-sets/acs-5year/2023.html); retain exact query, variable IDs and vintage | Combine state and county FIPS, preserving leading zeros; derive poverty rate only from documented numerator and denominator |
| CDC PLACES | County-level age-adjusted adult asthma (`CASTHMA`) and COPD (`COPD`) prevalence estimates from a specifically recorded release | [CDC PLACES](https://www.cdc.gov/places/); retain release identifier, URL, measurement year and variable definitions | Normalize `LocationID` to county FIPS, filter valid county rows and relevant measures, reshape long-to-wide if needed |

We will validate actual row counts and key structure using the downloaded files rather than relying on preliminary provider counts. We will not use Kaggle copies. No more detailed demographic variables are required for the planned exploratory comparisons. ACS estimates and CDC modeled estimates must be identified as estimates rather than raw individual observations.

**County-selection protocol:**

1. Standardize all geographic identifiers to five-character text values under `county_fips`; retain original keys for auditing.
2. Validate one row per county in the prepared EPA/ACS source and one row per county per target measure in CDC before pivoting; document and resolve duplicates without silently dropping conflicting records.
3. Produce a source-level coverage table and an integrated county-key inventory (including counties absent from EPA). Use left/outer joins for coverage assessment as appropriate, and explicitly construct complete-case subsets only for particular analyses.
4. Record per-variable missingness and excluded county FIPS with exclusion reasons; distinguish no EPA monitor, unmatched geographic key, invalid measurement, and missing socioeconomic/health indicators.
5. Document the actual universe of county/county-equivalent geography used for reporting after inspecting source coverage.

All source files, curated outputs, issue logs, lookup tables and coverage summaries will have clear provenance and stable repository paths.

## 5. Methods, Data Quality, Ethics, and Reproducibility

### 5.1 Acquisition, integrity, and provenance

Each source-specific acquisition process will record the official source URL/API request, access/retrieval date, release/vintage, filename, file size if available, and SHA-256 checksum. Immutable raw data will be stored under `data/raw/` when repository size and usage terms permit; otherwise reproducible download instructions or a permitted external data location will be provided. Re-runs will avoid silently overwriting raw inputs without recording a version or hash. Source reuse terms and attribution will be documented.

### 5.2 Quality assessment and cleaning

For each individual source, we will report four data-quality dimensions: **accuracy** (valid ranges, units, geographic codes and provider definitions), **completeness** (null fields and geographic coverage), **timeliness/currency** (reference period, release date, acquisition date), and **consistency** (schema, naming, FIPS formats, duplicates, measurement definitions). A quality/cleaning log will record detected issues, decisions and remaining uncertainties.

Cleaning will include type conversion, zero-padding valid geographic codes, explicit missing-value handling, inspection of EPA state/county name crosswalks, and selection/pivoting of CDC `MeasureId` values. Post-integration checks will validate uniqueness of `county_fips`, prevent unintended many-to-many joins, quantify records retained or lost, and recheck completeness and plausibility. In particular, **missing EPA AQI is not a zero measurement**.

### 5.3 Exploratory analysis and interpretation

We will generate basic distributions, coverage/missingness summaries, descriptive correlations and county-level plots involving median AQI, median household income, poverty rate, asthma prevalence and COPD prevalence. Each figure will identify the sample size and eligibility rules. Analyses will use available comparable observations, and conclusions will acknowledge nonrandom monitor placement, ecological aggregation, ACS sampling uncertainty, CDC model-based estimates, and temporal discrepancies. The project will not make causal or individual-level health claims.

### 5.4 Concrete reproducibility protocol (added after Milestone 2 feedback)

The repository will provide a runnable entry point (`run_all.py` **or** a `Snakefile`, selected after the team's implementation is reviewed), along with modular acquisition, cleaning, integration, QA and analysis steps. The final README will specify:

1. The source data versions, exact links/API queries, usage conditions, retrieval dates and expected checksums.
2. The Python version and installation commands using version-pinned `requirements.txt` (or an equivalent exported environment manifest).
3. The working directory, inputs/outputs for each stage, and a single documented invocation to regenerate results, using relative rather than machine-specific paths.
4. The expected output filenames, county coverage and basic assertions (unique five-digit FIPS, valid values, expected column set), to identify a failed or incomplete run.
5. How to regenerate quality tables and figures and verify that saved outputs correspond to documented inputs. If access constraints prevent automated downloads, the instructions will describe the manual step and checksum verification clearly.

A team member other than the author of each stage will attempt a **fresh-clone reproduction test** before the final release. Any non-reproducible steps or manual interventions will be disclosed. The repository will also include a data dictionary (field definitions, units, geographic grain, reference period, missingness codes) and structured machine-readable metadata where feasible. These are planned deliverables, **not claims that the corresponding scripts already exist**.

## 6. Updated Timeline and Deliverables

*Targets derive from the original Milestone 2 plan. Actual completion dates, blockers and owner confirmations belong in `StatusReport.md`; course deadlines must be checked against Canvas.*

| Target | Task and verifiable artifact | Lead / support | Status at this revision |
|---|---|---|---|
| Completed at Milestone 2 | Define topic, source candidates, roles, timeline and initial `ProjectPlan.md` | All; Samuel documents | Initial plan submitted; 19/20 feedback received |
| By Nov 18 | Confirm actual progress with each member; collect source versions, scripts and preliminary checks; publish links in `StatusReport.md` | All; Samuel coordinates | Awaiting team confirmation |
| By Nov 19 (interim target) | Summarize per-source quality, missingness, obstacles and updated schedule; update plan, commit individual contribution summaries and create status-report release | Source leads and Jashan; Samuel coordinates | In progress / evidence to be confirmed |
| Late Nov | Finish acquisition, cleaning, FIPS crosswalk, long-to-wide CDC transformation, integration and source/merged QA | Rex, Tergel, Jashan | Not independently verified |
| Early Dec | Generate descriptive analysis and at least one visualization, data dictionary, source/variable metadata and reproducibility instructions | Jashan analyzes; Samuel documents; all review | Planned |
| By Dec 8 (final target) | Test from a fresh clone, verify hashes/outputs, finalize README and provenance, commit deliverables, make final release | All | Planned |

## 7. Milestone 2 Feedback and Plan Changes

The Milestone 2 plan received **19/20**. Feedback on the goal and planned approach asked the team to clarify **which U.S. counties are in scope**, explain **how the work will be reproducible**, and provide a **more focused research direction**. The original dataset choices and broad research theme remain unchanged, but this revision addresses those concerns explicitly:

- **County scope:** Section 1 now distinguishes the broad coverage universe from the subset of counties eligible for analyses using AQI. Section 4 sets out an auditable inclusion/exclusion and FIPS inventory protocol.
- **Research focus:** Section 3 identifies a primary descriptive question and limits the tested variables to median AQI, household income, poverty, and adult asthma/COPD prevalence, with geographic coverage as a secondary curation question.
- **Reproducibility:** Section 5.4 specifies source versions and checksums, dependency pinning, a runnable entry point, explicit inputs/outputs, QA assertions, and independent fresh-clone testing.

These are **revisions to the intended method**; the final status of code and datasets must be confirmed against repository artifacts and individually authored team updates. Any additional grading feedback should also be incorporated when available.

## 8. Constraints, Risks, and Open Items

- **Geographic gaps and selection bias:** EPA monitoring availability is uneven; report unmonitored counties separately and limit interpretation to observed counties for AQI analyses.
- **Temporal alignment:** ACS 2023 five-year estimates, EPA 2023 AQI and the selected CDC PLACES release are not necessarily contemporaneous. Record the reference periods explicitly and avoid claims about changes over time.
- **Geographic identifiers and joins:** EPA name-to-FIPS crosswalks and county-equivalent naming can be ambiguous; review unmatched records and test uniqueness before and after every merge.
- **Estimated versus measured quantities:** ACS survey values and CDC modeled prevalence are not direct measurement equivalents to monitored EPA AQI; document uncertainty and provenance.
- **Workflow portability and data volume:** Verify source URLs, API rules, dependencies and external-data access, and preserve hashes/paths for reruns.
- **Team confirmation needed:** Actual source acquisitions, file paths, measured coverage, quality results, integration progress and any revised deadlines must be reported by the responsible members before the status report is finalized.

## Preliminary Sources

- U.S. Environmental Protection Agency. *AirData: Download Data Files*. https://aqs.epa.gov/aqsweb/airdata/download_files.html
- U.S. Census Bureau. *2023 ACS 5-Year Data via API*. https://www.census.gov/data/developers/data-sets/acs-5year/2023.html
- Centers for Disease Control and Prevention. *PLACES: Local Data for Better Health*. https://www.cdc.gov/places/
- IS 477. *Course Project Overview & Instructions* (updated September 16, 2026), course-provided document.
