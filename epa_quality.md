# EPA 2023 Data Quality Report
## Dataset
- Source: EPA AirData, Annual AQI by County (2023)
- Records: 993
- Columns: 18
## Quality Assessment
- **Accuracy**: All 993 records contain valid, non-negative `Median AQI` values ranging from 3 to 77 (mean: 41.28, median: 43). However, 8 counties have `Max AQI` values above 500 (up to 1,829 in Mono County, CA). These extreme values may reflect real pollution events, such as wildfires, and will be retained for further analysis.

- **Completeness**: There are 0 missing values across all 18 columns. However, the `Days with AQI` values range from 55 to 365 days (median: 363), showing differences in monitoring coverage across counties.

- **Timeliness**: All records are from 2023, based on the EPA source release dated June 25, 2026. This matches the 2023 reference year used for integration 

- **Consistency**: There are 0 duplicate rows and 0 duplicate `(State, County)` pairs. However, 10 records belong to non-U.S. The dataset also contains text-based `State` and `County` names without numeric FIPS codes. These issues will be addressed through jurisdiction filtering and a standardized name-to-FIPS lookup in the next stage.

## Median AQI Statistics
- Mean: 41.28
- Median: 43
- Minimum: 3
- Maximum: 77