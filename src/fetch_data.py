"""
Fetches the real data behind the Ozhand Chart.

Sources:
  - GDP per capita, PPP (current international $): World Bank API
  - Top-decile income share (before tax): World Inequality Database,
    via Our World in Data's grapher CSV endpoint
  - Gini coefficient (before tax): World Inequality Database,
    via the same OWID endpoint

Run:
    pip install -r requirements.txt
    python src/fetch_data.py

Writes data/ozhand_data_live.csv. Compare against data/ozhand_data.csv
(the snapshot used in the manuscript) to check for revisions.
"""

import csv
import io
import sys
import requests

COUNTRIES = {"USA": "United States", "DEU": "Germany", "GBR": "United Kingdom"}
YEARS = [1990, 2010, 2020, 2024]

WB_URL = (
    "https://api.worldbank.org/v2/country/{iso3}/indicator/NY.GDP.PCAP.PP.CD"
    "?format=json&date=1990:2024&per_page=1000"
)
WID_TOP10_URL = (
    "https://ourworldindata.org/grapher/incomes-of-the-richest.csv"
    "?v=1&csvType=full&useColumnShortNames=false&quantile=_10&welfare_type=before_tax"
)
WID_BOTTOM50_URL = (
    "https://ourworldindata.org/grapher/incomes-of-the-richest.csv"
    "?v=1&csvType=full&useColumnShortNames=false&quantile=_10_40_50&welfare_type=before_tax"
)
WID_GINI_URL = (
    "https://ourworldindata.org/grapher/gini-coefficient-wid.csv"
    "?v=1&csvType=full&useColumnShortNames=false&welfare_type=before_tax"
)


def fetch_gdp_per_capita():
    """Returns {iso3: {year: value}}"""
    out = {}
    for iso3 in COUNTRIES:
        r = requests.get(WB_URL.format(iso3=iso3), timeout=30)
        r.raise_for_status()
        rows = r.json()[1]
        out[iso3] = {
            int(row["date"]): row["value"]
            for row in rows
            if row["value"] is not None and int(row["date"]) in YEARS
        }
    return out


def fetch_wid_series(url, target_col=None):
    """Parses an OWID/WID grapher CSV into {country_name: {year: value}}.
    If target_col is given, use that column; otherwise use the first data column."""
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    reader = csv.DictReader(io.StringIO(r.text))
    non_key_cols = [c for c in reader.fieldnames if c not in ("Entity", "Code", "Year")]
    value_col = target_col if target_col in non_key_cols else non_key_cols[0]
    out = {}
    for row in reader:
        name = row["Entity"]
        if name not in COUNTRIES.values():
            continue
        try:
            year = int(row["Year"])
            val = float(row[value_col])
        except (ValueError, TypeError):
            continue
        out.setdefault(name, {})[year] = val
    return out


def nearest_year(available_years, target):
    return min(available_years, key=lambda y: abs(y - target))


def main():
    print("Fetching World Bank GDP per capita PPP ...", file=sys.stderr)
    gdp = fetch_gdp_per_capita()
    print("Fetching WID top-decile income share ...", file=sys.stderr)
    top10 = fetch_wid_series(WID_TOP10_URL)
    print("Fetching WID poorest-50% income share ...", file=sys.stderr)
    bottom50 = fetch_wid_series(WID_BOTTOM50_URL, "Poorest 50%")
    print("Fetching WID Gini coefficient ...", file=sys.stderr)
    gini = fetch_wid_series(WID_GINI_URL)

    rows = []
    for iso3, name in COUNTRIES.items():
        for year in YEARS:
            if year not in gdp.get(iso3, {}):
                continue
            t10_years = list(top10.get(name, {}).keys())
            b50_years = list(bottom50.get(name, {}).keys())
            g_years = list(gini.get(name, {}).keys())
            t10_year = nearest_year(t10_years, year) if t10_years else None
            b50_year = nearest_year(b50_years, year) if b50_years else None
            g_year = nearest_year(g_years, year) if g_years else None
            rows.append(
                {
                    "country": name,
                    "iso3": iso3,
                    "year": year,
                    "mean_income_ppp": round(gdp[iso3][year], 2),
                    "top10_share_pct": top10[name][t10_year] if t10_year else "",
                    "top10_share_year": t10_year or "",
                    "bottom50_share_pct": bottom50[name][b50_year] if b50_year else "",
                    "bottom50_share_year": b50_year or "",
                    "gini_before_tax": gini[name][g_year] if g_year else "",
                    "gini_year": g_year or "",
                }
            )

    out_path = "data/ozhand_data_live.csv"
    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
