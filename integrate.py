"""Join the EPA, CDC PLACES, and ACS county files on `county_fips` and report coverage.

Inputs
  data/processed/epa_aqi_2023_fips.csv          (from epa_fips.py)
  data/raw/acs_cdc/places_2025_age_adjusted_respiratory.csv
  data/raw/acs_cdc/acsdt5y2023-*.dat            (optional until the ACS files are in the repo)

Outputs (data/processed/)
  county_integrated.csv   one row per county_fips, outer join, with in_epa/in_cdc/in_acs flags
  coverage_summary.csv    counts for each source and each overlap

Run from the repo root after epa_fips.py:  python integrate.py
"""
import csv
import re
from pathlib import Path

import pandas as pd

PROCESSED = Path("data/processed")
RAW = Path("data/raw/acs_cdc")
EPA_FILE = PROCESSED / "epa_aqi_2023_fips.csv"
CDC_FILE = RAW / "places_2025_age_adjusted_respiratory.csv"
ACS_TABLES = {
    "B01003": {"B01003_E001": "population"},
    "B19013": {"B19013_E001": "median_household_income"},
    "B17001": {"B17001_E001": "poverty_universe", "B17001_E002": "below_poverty"},
}
ACS_MISSING = {-111111111, -222222222, -333333333, -555555555, -666666666, -888888888, -999999999}
FIPS = re.compile(r"[0-9]{5}")

EPA_COLUMNS = ["county_fips", "State", "County", "Days with AQI", "Median AQI", "Max AQI", "90th Percentile AQI"]


def require_unique(df, name):
    bad = df["county_fips"][~df["county_fips"].str.fullmatch(FIPS)]
    if not bad.empty:
        raise ValueError(f"{name}: invalid county_fips values {bad.tolist()[:5]}")
    dupes = df["county_fips"][df["county_fips"].duplicated()]
    if not dupes.empty:
        raise ValueError(f"{name}: duplicate county_fips {dupes.tolist()[:5]}")


def load_epa():
    epa = pd.read_csv(EPA_FILE, dtype={"county_fips": str})[EPA_COLUMNS]
    epa = epa.rename(columns={
        "State": "epa_state", "County": "epa_county", "Days with AQI": "aqi_days",
        "Median AQI": "median_aqi", "Max AQI": "max_aqi", "90th Percentile AQI": "p90_aqi",
    })
    require_unique(epa, "EPA")
    return epa


def load_cdc():
    cdc = pd.read_csv(CDC_FILE, dtype={"locationid": str})
    cdc = cdc[cdc["locationid"] != "59"]  # two U.S. total rows
    wide = cdc.pivot(index="locationid", columns="measureid", values="data_value").reset_index()
    wide.columns.name = None
    wide = wide.rename(columns={"locationid": "county_fips", "CASTHMA": "asthma_pct", "COPD": "copd_pct"})
    names = cdc.drop_duplicates("locationid").set_index("locationid")[["stateabbr", "locationname"]]
    wide = wide.join(names, on="county_fips").rename(columns={"stateabbr": "cdc_state", "locationname": "cdc_county"})
    require_unique(wide, "CDC")
    return wide


def load_acs():
    paths = {table: RAW / f"acsdt5y2023-{table.lower()}.dat" for table in ACS_TABLES}
    missing = [p.name for p in paths.values() if not p.exists()]
    if missing:
        print(f"ACS skipped: {', '.join(missing)} not found in {RAW}/")
        return None
    frames = []
    for table, fields in ACS_TABLES.items():
        df = pd.read_csv(paths[table], sep="|", dtype=str, usecols=["GEO_ID", *fields])
        df = df[df["GEO_ID"].str.startswith("0500000US")]
        df["county_fips"] = df["GEO_ID"].str[-5:]
        for field in fields:
            df[field] = pd.to_numeric(df[field]).where(lambda s: ~s.isin(ACS_MISSING))
        frames.append(df.drop(columns="GEO_ID").rename(columns=fields).set_index("county_fips"))
    acs = pd.concat(frames, axis=1, join="outer").reset_index()
    acs["poverty_rate_pct"] = 100 * acs["below_poverty"] / acs["poverty_universe"]
    require_unique(acs, "ACS")
    return acs


def main():
    epa, cdc, acs = load_epa(), load_cdc(), load_acs()

    merged = epa.assign(in_epa=True).merge(
        cdc.assign(in_cdc=True), on="county_fips", how="outer", validate="one_to_one")
    if acs is not None:
        merged = merged.merge(acs.assign(in_acs=True), on="county_fips", how="outer", validate="one_to_one")
    flags = [c for c in ("in_epa", "in_cdc", "in_acs") if c in merged]
    merged[flags] = merged[flags].astype("boolean").fillna(False).astype(bool)
    require_unique(merged, "merged")
    merged = merged.sort_values("county_fips")

    rows = [
        ("EPA counties with a FIPS code", int(merged["in_epa"].sum())),
        ("CDC PLACES counties", int(merged["in_cdc"].sum())),
        ("Counties in EPA and CDC", int((merged["in_epa"] & merged["in_cdc"]).sum())),
        ("EPA counties missing from CDC", int((merged["in_epa"] & ~merged["in_cdc"]).sum())),
        ("CDC counties with no EPA AQI", int((~merged["in_epa"] & merged["in_cdc"]).sum())),
        ("EPA and CDC with median AQI, asthma, and COPD all present",
         int((merged["in_epa"] & merged["in_cdc"] & merged[["median_aqi", "asthma_pct", "copd_pct"]].notna().all(axis=1)).sum())),
    ]
    if acs is not None:
        all_three = merged["in_epa"] & merged["in_cdc"] & merged["in_acs"]
        rows += [
            ("ACS counties", int(merged["in_acs"].sum())),
            ("Counties in all three sources", int(all_three.sum())),
        ]
    rows.append(("Rows in integrated file", len(merged)))

    PROCESSED.mkdir(parents=True, exist_ok=True)
    merged.to_csv(PROCESSED / "county_integrated.csv", index=False)
    with (PROCESSED / "coverage_summary.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["measure", "count"])
        writer.writerows(rows)

    for label, count in rows:
        print(f"{label}: {count:,}")
    gap = merged[merged["in_epa"] & ~merged["in_cdc"]]
    print("\nEPA counties missing from CDC, by state:")
    print(gap["epa_state"].value_counts().to_string())


if __name__ == "__main__":
    main()
