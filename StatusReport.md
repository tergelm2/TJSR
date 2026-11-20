# Milestone 3 - Interim Status Report

**Project:** Air Quality, Socioeconomic Conditions, and Respiratory Health Across U.S. Counties  
**Course:** IS 477 - Data Management, Curation & Reproducibility (Fall 2026)  
**Reporting date:** November 19, 2026  
**Team:** Rex Li (@YalinLisys), Tergel Myagmarsaikhan (@tergelm2), Jashan Takhar (@jashtakhar), Samuel Kang (@smukng)  
**Repository:** [TJSR](https://github.com/tergelm2/TJSR)

## 1. Project overview and scope

Our project investigates county-level relationships among measured air quality, socioeconomic conditions, and modeled respiratory health outcomes across the United States. The intended data sources remain the U.S. Environmental Protection Agency (EPA) 2023 county-level Annual Air Quality Index (AQI) summary, the U.S. Census Bureau 2023 American Community Survey (ACS) five-year estimates, and CDC PLACES estimates of adult asthma and chronic obstructive pulmonary disease (COPD) prevalence. Our integration key is a standardized five-character county FIPS code. We seek to describe associations and the geographic coverage of the sources, not causal effects or nationally representative effects of air pollution.

The research questions and initially proposed processing steps are documented in [ProjectPlan.md](ProjectPlan.md). The research questions concern environmental and socioeconomic associations with estimated asthma/COPD prevalence, as well as integration-related coverage and missingness.

## 2. Progress against the project plan

### 2.1 Project definition, roles, and source selection

**Status: Complete.** The [Milestone 2 plan](ProjectPlan.md), revised after the Milestone 2 feedback (Section 4), identifies the research questions, named team responsibilities, source agencies, core variables, county-level geographic unit, and major limitations. EPA data are intended to provide median AQI; ACS to provide total population, median household income, and poverty-related measures; and CDC PLACES to provide age-adjusted asthma and COPD estimates. The CDC release is now confirmed as the December 2025 PLACES county release (`swc5-untb`), which uses 2023 BRFSS data. **Evidence:** [ProjectPlan.md](ProjectPlan.md) · [CDC/ACS source notes](data/raw/acs_cdc/source_notes.md)

### 2.2 Source acquisition, integrity, and provenance

**Status: Complete.**

EPA acquisition completed.  Rex downloaded the official 2023 EPA Annual AQI by County dataset and documented its source, download date, and version information. The original ZIP file was preserved, and its SHA-256 checksum was calculated and recorded. The dataset contains 993 records and 18 columns. EPA acquisition artifacts and scripts are available in the repository: [EPA source notes](data/raw/epa_source_notes.md) · [Raw file](data/raw/annual_aqi_by_county_2023.zip) · [Hash script](hash.py)

Tergel downloaded the ACS and CDC data on November 19. The ACS files are tables B01003 (population), B19013 (median household income), and B17001 (poverty). The CDC download contains the age-adjusted asthma and COPD rows. We kept the CDC download in the repo and recorded the download links and SHA-256 checksums for all four files. [Download details](data/raw/acs_cdc/sources.json)

### 2.3 Pre-integration quality assessment

**Status: Complete.**

EPA quality assessment completed. Rex used Python to examine the 2023 EPA dataset for missing values, duplicate records, invalid negative Median AQI values.... All finding documented in [EPA Quality Report](epa_quality.md) It covers four aspects. Accuracy: No negative Median AQI values were found, but 8 Max AQI values exceed 500. Completeness: No missing values were found, although monitoring coverage varies from 55 to 365 days. Timeliness: All records cover 2023. Consistency: No duplicate records were found, but 10 records belong to non-U.S. or territory jurisdictions. [Quality script](quality.py). County FIPS mapping for the EPA file is now done (Section 2.4).


All three ACS tables had the same 3,222 unique county and county-equivalent FIPS codes. Two counties had missing income estimates. Population and poverty fields were complete. The CDC download had 5,916 rows, including two U.S. totals. The county rows covered 2,957 counties with one row per measure and county. CDC suppressed both estimates for Loving County, Texas (`48301`). All observed prevalence values and calculated poverty rates were within 0%-100%. [Source notes and results](data/raw/acs_cdc/source_notes.md) · [Quality check script](acs_cdc.py)

### 2.4 Cleaning and geographic-key standardization

**Status: Complete for EPA; ACS/CDC key checks built into integration.** The pipeline standardizes state/county identifiers into zero-padded five-character `county_fips` strings, normalizes missing values and numeric types, and resolves repeated observations at the county/measure level. EPA county names may need FIPS lookup; CDC requires filtering `MeasureId` and age-adjusted observations before pivoting. Log reproducible corrections on derived data. Unmatched county identifiers are reported rather than silently discarded.

The EPA file only has state and county names, so Jashan wrote [epa_fips.py](epa_fips.py) to add FIPS codes. It trims trailing spaces (some Alaska names had them), drops the Mexico and Virgin Islands rows, and looks up each county in the Census 2020 county list from the `addfips` package. Seven names needed a manual fix, mostly where a county and an independent city share a name (for example, "Saint Louis" in Missouri first matched St. Louis city, which collided with EPA's separate "St. Louis City" row). The fixes and the reason for each are in [epa_fips_overrides.csv](data/lookup/epa_fips_overrides.csv). The script stops if two EPA rows end up with the same FIPS code.

Before/after: 993 EPA rows → 2 dropped as outside the U.S. states, D.C., and Puerto Rico → 991 rows, all with a unique FIPS code (984 by lookup, 7 by override). **Evidence:** [epa_fips.py](epa_fips.py) · [override table](data/lookup/epa_fips_overrides.csv) · [EPA with FIPS](data/processed/epa_aqi_2023_fips.csv) · [excluded rows](data/processed/epa_unmatched.csv). The ACS and CDC files already use five-digit FIPS codes; [integrate.py](integrate.py) checks their format and uniqueness when it loads them.

### 2.5 Integration and post-integration quality assessment

**Status: EPA + CDC join complete; ACS join written but not yet run.** Jashan leads the pandas-based merge and verification of one record per county. [integrate.py](integrate.py) pivots the CDC file from long to wide (one row per county with `asthma_pct` and `copd_pct`), checks that each source has one row per FIPS code, and does an outer join with `validate="one_to_one"` so any row multiplication fails the run. Each row gets `in_epa`, `in_cdc`, and `in_acs` flags, so a county without an EPA monitor shows up as missing instead of being dropped or set to zero.

Verified results ([coverage_summary.csv](data/processed/coverage_summary.csv), [county_integrated.csv](data/processed/county_integrated.csv)):

| Measure | Counties |
|---|---|
| EPA counties with a FIPS code | 991 |
| CDC PLACES counties | 2,957 |
| In both EPA and CDC | 912 |
| EPA counties with no CDC match | 79 |
| CDC counties with no EPA AQI | 2,045 |

All 912 matched counties have median AQI, asthma, and COPD values. The 79 EPA counties without a CDC match are in Pennsylvania (38), Kentucky (25), Connecticut (8), and Puerto Rico (8); see Section 5. The ACS join is in the script, but the ACS `.dat` files are not in the repository yet (Section 5), so the script currently skips ACS. Once the files are available we will rerun it and add three-source counts and the post-integration quality assessment.

### 2.6 Exploratory analysis and visualizations

**Status: Not started (depends on the ACS join).** Planned analysis uses descriptive statistics, correlations, scatter plots, and coverage summaries. Figures need units, reference periods, sample sizes, and missing-data qualifications; correlations are not causal. Jashan will build summary statistics, a correlation table, and scatter plots of median AQI, income, and poverty against asthma and COPD for the matched counties, with the sample size stated on each figure. The current analytic sample is the 912 EPA-CDC counties in [county_integrated.csv](data/processed/county_integrated.csv), before the ACS join.

### 2.7 Documentation, metadata, and reproducibility

**Status: In progress.** Samuel coordinates documentation and metadata. Final deliverables include a data dictionary, machine-readable metadata, citations, dependency versions, and a reproducible `README.md`. A modular entry point (`run_all.py` or `Snakefile`) should sequence data acquisition, validation, cleaning, integration, and results. Samuel will check repository links and clean-clone reproducibility. So far, [requirements.txt](requirements.txt) lists the packages the current scripts use. The README, data dictionary, metadata file, and `run_all.py` are not started yet; the current run order is `acs_cdc.py`, `quality.py`, `epa_fips.py`, then `integrate.py`.

## 3. Revised timeline and ownership

Completed rows show the date the work was finished; other dates are targets.

| Task / deliverable | Owner | Status as verified here | Target completion |
|---|---|---|---|
| Research questions, roles, and approved scope in `ProjectPlan.md` | All; Samuel coordinates | Complete: plan revised after Milestone 2 feedback | November 16 |
| EPA download, provenance, hashes | Rex | Downloaded the 2023 EPA air quality dataset and documented its source, download data, and relevent information. I also recorded the SHA-256.| Completed on November 18, 2026 |
| ACS and CDC downloads, variables, provenance, hashes | Tergel | Downloaded both sources and recorded [file details and checksums](data/raw/acs_cdc/sources.json). | Completed November 19, 2026 |
| Pre-merge quality reports and cleaning rules | Rex, Tergel, Jashan | Rex: Completed the EPA data quality assessment. the dataset contains 993 records and 18 columns, with no missing values, duplicate records, or negative median AQI. Further cleaning and FIPS pending will be done during Thanksgiving vacation. Tergel completed the [ACS and CDC source checks](data/raw/acs_cdc/source_notes.md). | Rex: Further EPA data cleaning and county FIPS mapping are planned to be completed by November 29, 2026. Tergel completed the source checks on November 19, 2026. |
| Standardized FIPS identifiers and county-level integration | Jashan, source leads | EPA FIPS mapping and EPA + CDC join complete ([epa_fips.py](epa_fips.py), [integrate.py](integrate.py)); ACS join waiting on ACS files | EPA + CDC completed November 19; ACS join by November 29 |
| Move ACS files to Box and add a checksum-verified download step | Tergel | Not started | November 24 |
| Connecticut handling decision (Section 5) | Jashan, Rex | Not started | November 29 |
| Initial coverage/missingness results | Jashan | EPA + CDC coverage complete ([coverage_summary.csv](data/processed/coverage_summary.csv)); three-source counts after ACS join | EPA + CDC completed November 19; three-source by November 29 |
| Documentation inventory and draft metadata | Samuel | Not started; `requirements.txt` added | December 1 |
| Joint `StatusReport.md`, individual contribution commits, status release | All | Complete | November 19 |
| Final quality assessment, analysis, and visualizations | Jashan; all review | Planned | December 3 |
| Acquisition scripts and `run_all.py` | Rex, Tergel (acquisition); Jashan (`run_all.py`) | Planned | December 3 |
| Data dictionary, reproducible workflow, README, fresh-clone check | Samuel; all implement/test | Planned | December 6 |
| Final release and submission | All | Planned | December 8 |

## 4. Changes to the Project Plan and Milestone 2 Feedback

Our team received 19/20 on Milestone 2. The feedback identified three areas requiring improvement: defining the geographic scope of the study, clarifying the research focus, and explaining how the project would be reproducible.

To address these concerns, we revised `ProjectPlan.md` to specify county inclusion and exclusion criteria. Our study will assess geographic coverage across the EPA, ACS, and CDC datasets, while analyses involving AQI will be restricted to counties with valid and comparable measurements. Counties without EPA monitoring will be documented rather than assigned zero AQI values.

We also narrowed the primary research question to the relationships among county-level median AQI, household income, poverty rate, and estimated adult asthma and COPD prevalence. The analysis will remain descriptive and exploratory, without causal claims.

Finally, the revised plan describes our intended reproducibility workflow, including source documentation, SHA-256 checksums, standardized county FIPS identifiers, modular scripts, software dependencies, and instructions for regenerating the outputs. Some implementation components remain in progress and will be completed before the final project submission.

These revisions are documented in [ProjectPlan.md](ProjectPlan.md).

The integration work so far adds two scope notes. Anything using CDC data effectively covers 48 states plus D.C., because CDC has no estimates for Kentucky or Pennsylvania. Connecticut also needs separate handling (Section 5).

## 5. Challenges, mitigation, and remaining risks

**Geographic coverage.** EPA county AQI summaries are based on monitoring availability, whereas ACS and CDC estimates use broader geographic coverage. This creates potential selection bias and incomplete joins. *Status:* quantified. Only 991 counties have EPA AQI, compared with 2,957 in CDC, and among the 912 matched counties, 162 had AQI data on fewer than 274 days (75% of the year). Missing AQI is kept as missing with source flags. *Plan:* Rex and Jashan will choose a minimum-days rule before the analysis and report results with and without it.

**Cross-source reference periods.** The EPA 2023 report, ACS 2023 five-year estimates, and the selected CDC PLACES release may reflect different observation windows. *Plan:* Samuel will list each variable's reference period in the data dictionary, and the analysis will avoid claims about change over time.

**Key mismatches and duplication.** County names and FIPS formatting may differ, and long-form CDC measures can produce repeated county rows. *Resolved:* EPA names are mapped with a documented override table for 7 problem names (e.g., St. Louis, Baltimore, Roanoke, Fairfax, plus EPA's misspelled "Mayagnez"), and both scripts stop on duplicate FIPS codes or a non-one-to-one join.

**Reproducibility and reviewability.** Download methods, dependencies, file paths, and large-data storage requirements can prevent replication. Retain citations, hashes, pinned dependencies, relative paths, and run instructions. *Status:* partly addressed. Checksums are recorded and [requirements.txt](requirements.txt) is added. One concrete problem: `acsdt5y2023-b17001.dat` is 118 MB, over GitHub's 100 MB limit, so none of the ACS files were committed and `acs_cdc.py` fails on a fresh clone. *Plan:* Tergel will put the ACS files on Illinois Box with a download step that verifies the SHA-256 values in [sources.json](data/raw/acs_cdc/sources.json), and `run_all.py` will run the scripts in order.

**Connecticut county change.** EPA still reports Connecticut under its 8 old counties (`09001`-`09015`), but CDC and ACS 2023 use the 9 planning regions that replaced them in 2022 (`09110`-`09190`), so none of the 8 EPA rows match. *Plan:* there is no one-to-one mapping, so Connecticut will be left out of the AQI analysis and listed in the coverage table with this reason.

**No CDC estimates for Kentucky and Pennsylvania.** CDC did not publish 2023 BRFSS-based estimates for these two states, which removes 63 EPA counties; Puerto Rico (8) is also outside CDC's coverage. *Plan:* keep these counties in the coverage table as missing health data and note the gap when describing results.

## 6. Individual contributions and Git history

Each member must edit **their own** paragraph below and commit that change under their own GitHub account. Each statement must link completed work and that author's commit.

- **Rex Li (@YalinLisys): I downloaded the official 2023 EPA Annual AQI by County dataset and documented its source, version, and SHA-256. I also used Python to conduct a preliminary data quality assessment of 993 records and 18 columns. The results showed no missing values, duplicate records, or negative Median AQI values. I documented the findings and uploaded the dataset, Python code, and quality report to GitHub. County FIPS mapping and further cleaning will be finished before next report.
  Evidence: https://github.com/tergelm2/TJSR/blob/main/epa_quality.md
https://github.com/tergelm2/TJSR/blob/main/hash.py
https://github.com/tergelm2/TJSR/blob/main/quality.py
https://github.com/tergelm2/TJSR/blob/main/data/raw/epa_source_notes.md
https://github.com/tergelm2/TJSR/commit/3b83addc40631b7714810f76c10f654417058304
https://github.com/tergelm2/TJSR/commit/95783f7653d417ec8deba7f0beea454612a0b983

 - **Samuel Kang (@smukng):** I prepared and uploaded the initial `StatusReport.md` draft, coordinated the collection of progress updates from team members, and revised `ProjectPlan.md` based on the Milestone 2 feedback. My revisions clarified the county selection criteria, narrowed the research questions, and expanded the reproducibility plan. I am also responsible for organizing documentation, checking repository artifact links, and coordinating the final status-report release. Additional metadata, data dictionary, and reproducibility verification work remains planned for the final milestone.
   
- **Tergel Myagmarsaikhan (@tergelm2)** - I downloaded and documented the ACS and CDC files. I selected the ACS population, income, and poverty fields and the CDC age-adjusted asthma and COPD estimates. I checked the source files for missing estimates, duplicate county records, and out-of-range values. [Source notes](data/raw/acs_cdc/source_notes.md) · [Quality check script](acs_cdc.py)

- **Jashan Takhar (@jashtakhar):** I wrote [epa_fips.py](epa_fips.py), which gives every in-scope EPA county a FIPS code, and the [override file](data/lookup/epa_fips_overrides.csv) for the seven names the lookup got wrong. I also wrote [integrate.py](integrate.py), which reshapes the CDC data to one row per county, checks for duplicate keys, joins the sources, and writes the [integrated file](data/processed/county_integrated.csv) and [coverage counts](data/processed/coverage_summary.csv). While doing this I found the Connecticut planning-region mismatch and the Kentucky/Pennsylvania gap, and I filled in the cleaning, integration, timeline, and challenge sections of this report. Next I will run the ACS join, do the post-integration quality check, and make the first charts. [My commits](https://github.com/tergelm2/TJSR/commits?author=jashtakhar)

## 7. Next actions before the milestone release

Source owners have committed acquisition artifacts, and Jashan has committed the merge and coverage evidence. Each member must commit their own contribution statement. Push all work, create the `status-report` tag and release, then submit the **release URL** in Canvas.
