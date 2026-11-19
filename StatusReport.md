# Milestone 3 — Interim Status Report

**Project:** Air Quality, Socioeconomic Conditions, and Respiratory Health Across U.S. Counties  
**Course:** IS 477 — Data Management, Curation & Reproducibility (Fall 2026)  
**Reporting date:** November 16, 2026  
**Team:** Rex Li (@YalinLisys), Tergel Myagmarsaikhan (@tergelm2), Jashan Takhar (@jashtakhar), Samuel Kang (@smukng)  
**Repository:** [TJSR](https://github.com/tergelm2/TJSR)

> **Draft status notice:** The only implementation artifact verified on the repository's `main` branch as of this draft is [ProjectPlan.md](ProjectPlan.md). Statements below distinguish the agreed plan from **unverified progress**. Each lead must replace the `UPDATE REQUIRED` fields with accurate statuses and committed artifact links before this report is submitted. Do not submit this note unchanged.

## 1. Project overview and scope

Our project investigates county-level relationships among measured air quality, socioeconomic conditions, and modeled respiratory health outcomes across the United States. The intended data sources remain the U.S. Environmental Protection Agency (EPA) 2023 county-level Annual Air Quality Index (AQI) summary, the U.S. Census Bureau 2023 American Community Survey (ACS) five-year estimates, and CDC PLACES estimates of adult asthma and chronic obstructive pulmonary disease (COPD) prevalence. Our integration key is a standardized five-character county FIPS code. We seek to describe associations and the geographic coverage of the sources, not causal effects or nationally representative effects of air pollution.

The research questions and initially proposed processing steps are documented in [ProjectPlan.md](ProjectPlan.md). The research questions concern environmental and socioeconomic associations with estimated asthma/COPD prevalence, as well as integration-related coverage and missingness.

## 2. Progress against the project plan

### 2.1 Project definition, roles, and source selection

**Status: Planned scope documented; team confirmation UPDATE REQUIRED.** The [Milestone 2 plan](ProjectPlan.md) identifies the research questions, named team responsibilities, source agencies, core variables, county-level geographic unit, and major limitations. EPA data are intended to provide median AQI; ACS to provide total population, median household income, and poverty-related measures; and CDC PLACES to provide age-adjusted asthma and COPD estimates. The team must confirm the CDC release and scope. **Evidence to link:** updated [ProjectPlan.md](ProjectPlan.md) and any committed source inventory or meeting notes (`UPDATE REQUIRED: exact path`).

### 2.2 Source acquisition, integrity, and provenance

**Status: UPDATE REQUIRED — not verifiable from the current `main` tree.** Rex is responsible for EPA acquisition, while Tergel is responsible for ACS and CDC acquisition. Document each source URL, retrieval date, version, row count, and reuse conditions. The planned workflow computes SHA-256 checksums and preserves raw inputs. Link acquisition scripts and hashes rather than asserting downloads succeeded. **Evidence to link when available:** `data/raw/`, source-specific scripts, a retrieval log, and checksum records (`UPDATE REQUIRED: actual paths`). If files are too large to commit, record their stable source URLs, hashes, and reproducible retrieval instructions instead.

### 2.3 Pre-integration quality assessment

**Status: UPDATE REQUIRED.** Assess accuracy, completeness, timeliness, and consistency using geographic IDs, ranges, null counts, duplicate counts, reference periods, and units. In particular, a county without EPA monitoring must not be assigned an AQI of zero. CDC and ACS estimates require appropriate caveats. **Evidence to link when available:** profiling scripts, quality tables, issue logs, and a concise summary of concrete findings (`UPDATE REQUIRED: actual paths and results`). No counts or quality pass rates are asserted here without the outputs.

### 2.4 Cleaning and geographic-key standardization

**Status: UPDATE REQUIRED.** The intended pipeline standardizes state/county identifiers into zero-padded five-character `county_fips` strings, normalizes missing values and numeric types, and resolves repeated observations at the county/measure level. EPA county names may need FIPS lookup; CDC requires filtering `MeasureId` and age-adjusted observations before pivoting. Log reproducible corrections on derived data. **Evidence to link when available:** cleaning scripts, mapping tables, schema documentation, and before/after counts (`UPDATE REQUIRED: actual paths`). Unmatched county identifiers should be reported rather than silently discarded.

### 2.5 Integration and post-integration quality assessment

**Status: UPDATE REQUIRED.** Jashan leads the pandas-based merge and verification of one record per county. Validate key uniqueness before joining; afterward, inspect row multiplication, county coverage, missingness, and retained observations. Distinguish unavailable EPA measurements from other missing data. **Evidence to link when available:** integration script, merged output, coverage table, and quality metrics (`UPDATE REQUIRED: actual paths`). This report should eventually include verified numeric match/retention results, not estimates.

### 2.6 Exploratory analysis and visualizations

**Status: UPDATE REQUIRED.** Planned analysis uses descriptive statistics, correlations, scatter plots, and coverage summaries. Figures need units, reference periods, sample sizes, and missing-data qualifications; correlations are not causal. **Evidence to link when available:** analysis script, generated tables/figures, and the documented county sample (`UPDATE REQUIRED: actual paths`). These artifacts may still be in progress at the interim milestone.

### 2.7 Documentation, metadata, and reproducibility

**Status: Project plan exists; remaining artifacts UPDATE REQUIRED.** Samuel coordinates documentation and metadata. Final deliverables include a data dictionary, machine-readable metadata, citations, dependency versions, and a reproducible `README.md`. A modular entry point (`run_all.py` or `Snakefile`) should sequence data acquisition, validation, cleaning, integration, and results. Samuel will check repository links and clean-clone reproducibility. **Evidence to link when available:** `README.md`, data dictionary, metadata file, environment specification, and orchestration script (`UPDATE REQUIRED: actual paths`).

## 3. Revised timeline and ownership

Dates are working targets, not completion claims; verify against Canvas.

| Task / deliverable | Owner | Status as verified here | Target completion |
|---|---|---|---|
| Research questions, roles, and approved scope in `ProjectPlan.md` | All; Samuel coordinates | Plan documented; feedback update unverified | November 17 |
| EPA download, provenance, hashes | Rex | Downloaded the 2023 EPA air quality dataset and documented its source, download data, and relevent information. I also recorded the SHA-256.| November 17 |
| ACS and CDC downloads, variables, provenance, hashes | Tergel | UPDATE REQUIRED | November 17 |
| Pre-merge quality reports and cleaning rules | Rex, Tergel, Jashan | Rex: Completed the EPA data quality assessment. the dataset contains 993 records and 18 columns, with no missing values, duplicate records, or negative median AQI. Further cleaning and FIPS pending will be done during Thanksgiving vacation | November 18 |
| Standardized FIPS identifiers and county-level integration | Jashan, source leads | UPDATE REQUIRED | November 18 |
| Initial coverage/missingness results | Jashan | UPDATE REQUIRED | November 18 |
| Documentation inventory and draft metadata | Samuel | UPDATE REQUIRED | November 18 |
| Joint `StatusReport.md`, individual contribution commits, status release | All | In preparation | November 19 |
| Final quality assessment, analysis, and visualizations | Jashan; all review | Planned | December 3 |
| Data dictionary, reproducible workflow, README, fresh-clone check | Samuel; all implement/test | Planned | December 6 |
| Final release and submission | All | Planned | December 8 |

## 4. Changes to the project plan and Milestone 2 feedback

The scope remains limited to three ACS variables, two CDC outcomes, county FIPS integration, and noncausal descriptive analysis unless explicitly revised. **Milestone 2 instructor feedback has not been supplied for this draft.** Insert the feedback, resulting plan revisions, rationale, and relevant commits before submitting. If no feedback was provided, say that explicitly; do not imply instructor approval. Commit the revised plan with this report.

## 5. Challenges, mitigation, and remaining risks

**Geographic coverage.** EPA county AQI summaries are based on monitoring availability, whereas ACS and CDC estimates use broader geographic coverage. This creates potential selection bias and incomplete joins. Quantify coverage and preserve missingness.

**Cross-source reference periods.** The EPA 2023 report, ACS 2023 five-year estimates, and the selected CDC PLACES release may reflect different observation windows. Record vintages and qualify interpretation.

**Key mismatches and duplication.** County names and FIPS formatting may differ, and long-form CDC measures can produce repeated county rows. Normalize keys and verify join cardinality and duplicates.

**Reproducibility and reviewability.** Download methods, dependencies, file paths, and large-data storage requirements can prevent replication. Retain citations, hashes, pinned dependencies, relative paths, and run instructions. **Resolution status for each issue is UPDATE REQUIRED** once the responsible owner has evidence.

## 6. Individual contributions and Git history

Each member must edit **their own** paragraph below and commit that change under their own GitHub account. Each statement must link completed work and that author's commit.

- **Rex Li (@YalinLisys):** `UPDATE REQUIRED BY REX` — specify EPA acquisition, documentation, profiling, or cleaning completed, with commit and artifact links.
- **Tergel Myagmarsaikhan (@tergelm2):** `UPDATE REQUIRED BY TERGEL` — specify ACS/CDC acquisition, schema work, or validation completed, with commit and artifact links.
- **Jashan Takhar (@jashtakhar):** `UPDATE REQUIRED BY JASHAN` — specify integration, key harmonization, quality assessment, or preliminary analysis completed, with commit and artifact links.
- **Samuel Kang (@smukng):** `UPDATE REQUIRED BY SAMUEL` — describe personally completed documentation, plan revision, metadata/data-dictionary work, reproducibility testing, and report coordination; link commits and outputs. Do not claim that draft or planned deliverables are already final.

## 7. Next actions before the milestone release

Source owners should commit acquisition artifacts; Jashan should supply coverage and merge evidence; Samuel should incorporate feedback and link artifacts; and each member must commit their own contribution statement. Push all work, create the `status-report` tag and release, then submit the **release URL** in Canvas.
