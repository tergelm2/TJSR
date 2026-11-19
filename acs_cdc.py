"""Check the ACS and CDC downloads for Milestone 3."""

import csv
import json
import re
from hashlib import file_digest
from pathlib import Path


RAW = Path("data/raw/acs_cdc")
ACS_COUNTY_ID = re.compile(r"0500000US([0-9]{5})")
COUNTY_FIPS = re.compile(r"[0-9]{5}")
ACS_MISSING = {-111111111, -222222222, -333333333, -555555555, -666666666, -888888888, -999999999}
CDC_FILENAME = "places_2025_age_adjusted_respiratory.csv"


def check_downloads():
    manifest = json.loads((RAW / "sources.json").read_text(encoding="utf-8"))
    for source in manifest["files"]:
        path = RAW / source["filename"]
        with path.open("rb") as file:
            digest = file_digest(file, "sha256").hexdigest()
        if digest != source["sha256"]:
            raise ValueError(f"SHA-256 mismatch for {path.name}")
    print(f"Verified SHA-256 for {len(manifest['files'])} downloads.")


def read_acs_counties(table, fields):
    counties = {}
    with (RAW / f"acsdt5y2023-{table.lower()}.dat").open(encoding="utf-8-sig", newline="") as file:
        reader = csv.reader(file, delimiter="|")
        header = next(reader)
        geo_column = header.index("GEO_ID")
        field_columns = [header.index(field) for field in fields]
        for row in reader:
            county = ACS_COUNTY_ID.fullmatch(row[geo_column])
            if county is None:
                continue
            fips = county[1]
            if fips in counties:
                raise ValueError(f"{table}: duplicate county {fips}")
            estimates = []
            for column in field_columns:
                value = int(row[column]) if row[column] else None
                if value in ACS_MISSING:
                    value = None
                if value is not None and value < 0:
                    raise ValueError(f"{table}: negative estimate for {fips}")
                estimates.append(value)
            counties[fips] = estimates
    if not counties:
        raise ValueError(f"{table}: no county rows")
    return counties


def print_summary(label, values, decimals=0):
    missing = sorted(fips for fips, value in values.items() if value is None)
    observed = [value for value in values.values() if value is not None]
    print(f"{label}: {len(values):,} counties, {len(missing)} missing")
    if missing:
        print("  Missing FIPS: " + ", ".join(missing))
    if observed:
        print(f"  Range: {min(observed):,.{decimals}f} to {max(observed):,.{decimals}f}")


def check_acs():
    population = read_acs_counties("B01003", ("B01003_E001",))
    income = read_acs_counties("B19013", ("B19013_E001",))
    poverty = read_acs_counties("B17001", ("B17001_E001", "B17001_E002"))
    if population.keys() != income.keys() or population.keys() != poverty.keys():
        raise ValueError("The three ACS tables have different county keys")

    print_summary("ACS total population", {fips: row[0] for fips, row in population.items()})
    print_summary("ACS median household income", {fips: row[0] for fips, row in income.items()})
    rates = {}
    for fips, (total, below_poverty) in poverty.items():
        rates[fips] = None
        if total is None or below_poverty is None:
            continue
        if below_poverty > total:
            raise ValueError(f"B17001: poverty count exceeds its denominator for {fips}")
        if total > 0:
            rates[fips] = 100 * below_poverty / total
    print_summary("ACS poverty rate (%)", rates, decimals=2)


def check_cdc():
    measures = {"CASTHMA": {}, "COPD": {}}
    national_rows = 0
    with (RAW / CDC_FILENAME).open(encoding="utf-8-sig", newline="") as file:
        for row in csv.DictReader(file):
            fips = row["locationid"]
            measure = row["measureid"]
            if measure not in measures or row["datavaluetypeid"] != "AgeAdjPrv":
                raise ValueError(f"Unexpected CDC measure or estimate type for {fips}")
            if row["year"] != "2023" or row["data_value_unit"] != "%":
                raise ValueError(f"Unexpected year or unit for {fips}")
            if fips == "59" and row["stateabbr"] == "US":
                national_rows += 1
                continue
            if not COUNTY_FIPS.fullmatch(fips):
                raise ValueError(f"Invalid CDC county ID: {fips}")
            if fips in measures[measure]:
                raise ValueError(f"Duplicate CDC row for {fips}, {measure}")
            value = float(row["data_value"]) if row["data_value"] else None
            if value is not None and not 0 <= value <= 100:
                raise ValueError(f"CDC percentage out of range for {fips}, {measure}")
            measures[measure][fips] = value

    if not all(measures.values()):
        raise ValueError("The CDC download must include both measures")
    row_count = sum(len(values) for values in measures.values()) + national_rows
    print(f"CDC download: {row_count:,} rows, including {national_rows} U.S. totals")
    county_count = len(measures["CASTHMA"].keys() | measures["COPD"].keys())
    print(f"CDC county rows represent {county_count:,} distinct counties.")
    print_summary("CDC age-adjusted adult asthma (%)", measures["CASTHMA"], decimals=1)
    print_summary("CDC age-adjusted adult COPD (%)", measures["COPD"], decimals=1)


if __name__ == "__main__":
    check_downloads()
    check_acs()
    check_cdc()
