"""Attach five-digit county FIPS codes to the 2023 EPA Annual AQI by County file.

EPA publishes state and county names only. This script trims stray whitespace,
looks each name up in the Census 2020 county list bundled with the `addfips`
package, applies the hand-checked fixes in data/lookup/epa_fips_overrides.csv,
and writes matched and unmatched rows to data/processed/.

Run from the repo root:  python epa_fips.py
"""
import csv
from pathlib import Path

import addfips
import pandas as pd

EPA_ZIP = Path("data/raw/annual_aqi_by_county_2023.zip")
OVERRIDES = Path("data/lookup/epa_fips_overrides.csv")
OUT_DIR = Path("data/processed")

# Rows that are not U.S. states, D.C., or Puerto Rico and so have no county FIPS.
OUT_OF_SCOPE = {"Country Of Mexico", "Virgin Islands"}


def load_overrides():
    with OVERRIDES.open(encoding="utf-8", newline="") as file:
        return {(row["state"], row["county"]): row["county_fips"] for row in csv.DictReader(file)}


def main():
    epa = pd.read_csv(EPA_ZIP)
    rows_in = len(epa)
    epa["State"] = epa["State"].str.strip()
    epa["County"] = epa["County"].str.strip()

    out_of_scope = epa[epa["State"].isin(OUT_OF_SCOPE)]
    epa = epa[~epa["State"].isin(OUT_OF_SCOPE)].copy()

    lookup = addfips.AddFIPS(vintage=2020)
    overrides = load_overrides()

    def to_fips(row):
        key = (row["State"], row["County"])
        if key in overrides:
            return overrides[key], "override"
        fips = lookup.get_county_fips(row["County"], state=row["State"])
        return (fips, "addfips") if fips else (None, "unmatched")

    epa[["county_fips", "fips_method"]] = epa.apply(to_fips, axis=1, result_type="expand")

    matched = epa[epa["county_fips"].notna()]
    unmatched = epa[epa["county_fips"].isna()]

    dupes = matched[matched["county_fips"].duplicated(keep=False)]
    if not dupes.empty:
        raise ValueError(f"Two EPA rows mapped to the same FIPS:\n{dupes[['State', 'County', 'county_fips']]}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    matched.to_csv(OUT_DIR / "epa_aqi_2023_fips.csv", index=False)
    unmatched_report = pd.concat([
        unmatched.assign(reason="no FIPS match"),
        out_of_scope.assign(reason="outside U.S. states, D.C., and Puerto Rico"),
    ])[["State", "County", "reason"]]
    unmatched_report.to_csv(OUT_DIR / "epa_unmatched.csv", index=False)

    print(f"EPA rows read: {rows_in}")
    print(f"Dropped as out of scope: {len(out_of_scope)}")
    print(f"Matched to FIPS: {len(matched)} "
          f"({(matched['fips_method'] == 'addfips').sum()} lookup, {(matched['fips_method'] == 'override').sum()} override)")
    print(f"Unmatched: {len(unmatched)}")
    if not unmatched.empty:
        print(unmatched[["State", "County"]].to_string(index=False))


if __name__ == "__main__":
    main()
