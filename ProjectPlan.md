# Project Plan: Air Quality, Socioeconomic Conditions, and Respiratory Health Across U.S. Counties

**Course:** IS 477 — Data Management, Curation & Reproducibility  
**Milestone:** 2 — Project Plan (Draft for Team Review)  
**Status:** Proposed topic and responsibilities; subject to confirmation by all team members  
**Team repository:** https://github.com/tergelm2/TJSR  
**Canvas deadline:** [Confirm]

> **Team action required:** Please review the proposed scope and datasets, enter your own names in the responsibility table below, suggest edits through commits or pull requests, and confirm agreement in our group chat. This is a draft, **not** the approved final release. Each member should contribute a commit. Do not create the `project-plan` release until the team approves the revised plan.

## 1. Overview

This project proposes a reproducible county-level data curation workflow to explore the relationship between air quality, socioeconomic conditions, and estimated respiratory health outcomes in the United States. We will acquire three complementary datasets from original government sources: Environmental Protection Agency (EPA) county-level air quality data, U.S. Census Bureau American Community Survey (ACS) socioeconomic estimates, and Centers for Disease Control and Prevention (CDC) PLACES local health estimates. The intended unit of analysis is a U.S. county, linked using standardized five-character county FIPS identifiers.

We will document acquisition, integrity, quality assessment, cleaning, integration and exploratory analysis, paying particular attention to counties missing EPA monitoring. Deliverables will include a county-level dataset, quality metrics, visualization, data dictionary, metadata, and a reproducible modular workflow. We will not infer causality.

## 2. Team and Responsibilities

**Enter your name/username and confirm your role.** Member numbers are placeholders. Everyone should contribute commits and review reproducibility.

| Role | Member / GitHub username (fill in) | Proposed primary responsibility | Evidence of contribution |
|---|---|---|---|
| 1 — EPA source lead | Rex Li/@YalinLisys | Retrieve EPA county AQI data; document provenance and coverage; implement acquisition and EPA-specific cleaning | Source notes, acquisition/cleaning script, commits |
| 2 — ACS & CDC source lead | [Name / @username] | Retrieve ACS and PLACES data; check field definitions, geographic IDs, licenses, and source-specific missingness | Acquisition scripts, field notes, commits |
| 3 — Integration & quality lead | [Name / @username] | Define common schema and FIPS normalization; assess four quality dimensions before and after integration; implement joins and diagnostics | Integration/QA scripts, metrics, commits |
| 4 — Documentation & metadata lead | Samuel Kang / @smukng | Coordinate `ProjectPlan.md`, README, source citations, data dictionary and metadata; draft the timeline and constraints; help test `run_all.py` and organize the final release | Documentation files, metadata, reproducibility checks, commits |


## 3. Research Questions

1. How do available county-level air quality measures vary with poverty and household-income indicators?
2. How are air quality and socioeconomic indicators associated with CDC PLACES estimates of adult asthma and chronic obstructive pulmonary disease (COPD) prevalence among counties with comparable available records?
3. How does geographic coverage and missingness change when the EPA, ACS, and CDC datasets are standardized and integrated? Which counties are lost or lack one or more measures?



## 4. Proposed Datasets and Integration Design

| Source | Planned dataset and contribution | Proposed acquisition | Candidate join key / caveat |
|---|---|---|---|
| U.S. EPA | AirData annual county Air Quality Index (AQI) summary; air quality measures and observation coverage | Official EPA AirData download | State code + county code, normalized and zero-padded to county FIPS; monitored counties are a subset of all counties |
| U.S. Census Bureau | 2023 ACS 5-Year county estimates: population, income, and poverty-related variables | Official Census API | State FIPS + county FIPS; ACS figures are estimates with survey uncertainty |
| U.S. CDC | PLACES county-level adult asthma and COPD prevalence estimates, using a documented release | Official CDC PLACES data download/API | County FIPS; release year is not necessarily the measurement year for every indicator |

Official starting points: [EPA AirData](https://aqs.epa.gov/aqsweb/airdata/download_files.html), [2023 ACS 5-Year API](https://www.census.gov/data/developers/data-sets/acs-5year/2023.html), and [CDC PLACES](https://www.cdc.gov/places/).  We will inspect sample extracts, confirm at least 100 records per dataset, validate join keys, and record dataset versions. We will use no Kaggle repackaging.

The key is zero-padded five-character `county_fips`. EPA, ACS and CDC IDs will be standardized. We will validate county-key uniqueness and document how long-form CDC measures are reshaped.  We will document unmatched keys and coverage. 

## 5. Methods, Quality, Ethics, and Reproducibility

We follow acquisition, preservation, assessment, cleaning, integration, analysis and reuse. Raw files remain unchanged under `data/raw/`; outputs use separate directories. A codebook will describe fields, units, coverage and provenance.

An acquisition script for each source will retrieve data from the original provider when allowed, record source URLs and retrieval dates, and calculate SHA-256 checksums. We will check data licenses and redistribution terms and cite the agencies. We will not make individual-level or causal claims from aggregate data.

**Pre-integration quality assessment** will evaluate all four required dimensions for each input: *accuracy* (valid ranges, units, geographic codes, documented provider methods), *completeness* (missing values and geographic coverage), *timeliness* (measurement period, release year, and retrieval date), and *consistency* (type, units, naming, key formats, duplication, and within-dataset contradictions). Issues will be logged with corrective actions. We will distinguish unmonitored observations from zero measurements.

Scripts will normalize types and FIPS codes, handle missing values, and resolve duplicate county-measure rows before joining on `county_fips`. **Post-integration assessment** will repeat the four quality dimensions and report record retention, source coverage, key uniqueness, missingness, temporal compatibility, and plausibility of the integrated fields. Unexpected join multiplication will be diagnosed.

Analysis will provide summaries and at least one visualization, with coverage and model limitations disclosed. Separate scripts for each stage will be orchestrated by `run_all.py` or a `Snakefile`. Relative paths, `requirements.txt` with versions, a full reproduction procedure, a data dictionary, and Schema.org/DCAT/DataCite-style machine-readable metadata will support a clean-clone rerun. Oversized or restricted inputs will follow the course Box requirements.

## 6. Draft Timeline and Deliverables

*Dates below are sequencing targets; replace them with confirmed Canvas dates. Responsible members refer to the provisional role table.*

| Phase / target | Task and output | Lead / support |
|---|---|---|
| Before plan release | Team reviews topic, verifies source access and sample keys, fills names, confirms scope and deadline; revise and commit `ProjectPlan.md` | All; Role 4 coordinates |
| Early implementation | Acquire three source extracts; citations, licenses, retrieval log and SHA-256 manifest | Roles 1 & 2; Role 4 documents |
| Before interim status report | Profile each input on accuracy, completeness, timeliness and consistency; document issues and cleaning rules | Roles 1–3 |
| Mid-project | Implement and verify separate cleaning scripts, common schema and county-key integration | Role 3; Roles 1 & 2 |
| After integration | Reassess all four quality dimensions, quantify match rates/unmatched counties and review limitations | Role 3; all review |
| Before final release | Add limited analysis/visualization, data dictionary, metadata, `requirements.txt`, full README, and modular orchestrator | Role 4 coordinates documentation; all implement/test |
| Final verification | Fresh-clone end-to-end run, review citations/licenses and contribution history; make final release | All |

## 7. Constraints, Risks, and Open Gaps

- **Unequal geographic coverage:** EPA monitoring does not cover every county. We will report join coverage and avoid treating absent readings as zero or drawing nationally representative conclusions from monitored counties alone.
- **Temporal comparability:** EPA AQI, ACS 5-Year estimates, and CDC PLACES measures may have different reference periods. We will inspect provider documentation, preserve vintage fields, and interpret temporal mismatches cautiously.
- **Identifier and grain mismatch:** Geographic codes may require padding; CDC records may be long-form by measure. We will test uniqueness and cardinality and avoid many-to-many joins caused by unexamined duplicates.
- **Estimation and measurement limitations:** ACS has survey uncertainty; PLACES provides modeled prevalence; EPA monitors reflect available measurements. We will state these caveats and avoid causal language.
- **Access and reproducibility:** We must verify download endpoints, CSV/JSON schemas, record counts, licensing, file sizes, and whether API limits or credentials affect reruns. Requirements and data access will be documented; restricted or oversized files will use the prescribed Box workflow.
- **Items awaiting team confirmation:** Team member names and GitHub handles; exact measures/columns and source versions; precise period and county coverage; role allocation; Canvas milestone dates; final scope after a small join prototype.

## Team Confirmation Checklist

- [ ] All four members have reviewed this draft and proposed edits.
- [ ] Each member has filled in their name/GitHub username and confirmed a primary role.
- [ ] The three source extracts, record counts, license terms, and county-level join strategy have been checked.
- [ ] Research questions, selected data vintage, and limitations are agreed.
- [ ] Actual Canvas deadlines replace all placeholders.
- [ ] Individual edits are committed and pushed; the team approves creating the `project-plan` tag/release.

## Preliminary Sources

- U.S. Environmental Protection Agency. *AirData: Download Data Files*. https://aqs.epa.gov/aqsweb/airdata/download_files.html
- U.S. Census Bureau. *2023 ACS 5-Year Data via API*. https://www.census.gov/data/developers/data-sets/acs-5year/2023.html
- Centers for Disease Control and Prevention. *PLACES: Local Data for Better Health*. https://www.cdc.gov/places/
- IS 477. *Course Project Overview & Instructions* (updated September 16, 2026), course-provided document.
