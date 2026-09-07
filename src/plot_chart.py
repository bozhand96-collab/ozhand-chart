"""
Renders the Ozhand Chart (candlestick-inspired tube chart) from
data/ozhand_data.csv, one subplot per country, log-scale y-axis.

The tube ceiling is built from the real top-decile income share,
the floor from an approximate, roughly time-invariant bottom-decile
share (see README for why this remains an approximation).

Run:
    pip install -r requirements.txt
    python src/plot_chart.py
Writes ozhand_chart.png
"""

import csv
import matplotlib.pyplot as plt

DATA_PATH = "data/ozhand_data.csv"
OUT_PATH = "ozhand_chart.png"

COLORS = {
    "United States": "#185FA5",
    "Germany": "#0F6E56",
    "United Kingdom": "#993C1D",
}


def load_data():
    countries = {}
    with open(DATA_PATH) as f:
        for row in csv.DictReader(f):
            c = row["country"]
            b50 = row.get("bottom50_share_pct", "").strip()
            countries.setdefault(c, []).append(
                {
                    "year": int(row["year"]),
                    "mean": float(row["mean_income_ppp"]),
                    "top10": float(row["top10_share_pct"]),
                    "bottom10": float(row["bottom10_share_pct"]),
                    "bottom50": float(b50) if b50 else None,
                    "gini": float(row["gini_before_tax"]),
                }
            )
    return countries


def tube_bounds(points):
    years = [p["year"] for p in points]
    mean = [p["mean"] for p in points]
    hi = [p["mean"] * p["top10"] / 10 for p in points]
    # Floor: use the real bottom-50% share (average income of the bottom half)
    # when available; otherwise fall back to the approximate bottom-decile share.
    lo = [
        p["mean"] * p["bottom50"] / 50 if p["bottom50"] is not None
        else p["mean"] * p["bottom10"] / 10
        for p in points
    ]
    return years, mean, hi, lo


def main():
    countries = load_data()
    n = len(countries)
    fig, axes = plt.subplots(n, 2, figsize=(11, 3.4 * n))
    if n == 1:
        axes = [axes]

    for row, (name, points) in zip(axes, countries.items()):
        points.sort(key=lambda p: p["year"])
        years, mean, hi, lo = tube_bounds(points)
        color = COLORS.get(name, "#534AB7")

        for ax, scale in zip(row, ("log", "linear")):
            ax.fill_between(years, lo, hi, color=color, alpha=0.25, linewidth=0)
            ax.plot(years, mean, color=color, linewidth=3, marker="o")
            ax.plot(years, hi, color=color, linewidth=1, linestyle="--", alpha=0.7)
            ax.plot(years, lo, color=color, linewidth=1, linestyle="--", alpha=0.7)
            ax.set_yscale(scale)
            title_suffix = "log scale — for cross-country comparison" if scale == "log" \
                else "linear scale — true dollar proportions"
            ax.set_title(f"{name} ({title_suffix})", fontsize=10)
            ax.set_ylabel("Income, PPP $")
            for p in points:
                ax.annotate(
                    f"Gini {p['gini']:.3f}",
                    (p["year"], p["mean"]),
                    textcoords="offset points",
                    xytext=(0, 8),
                    fontsize=7,
                    ha="center",
                )

    for ax in axes[-1]:
        ax.set_xlabel("Year")
    fig.suptitle(
        "The Ozhand Chart — income growth and distribution, 1990-2024\n"
        "Left: log scale (compares countries). Right: linear scale (true dollar gaps).",
        fontsize=12,
    )
    fig.tight_layout()
    fig.savefig(OUT_PATH, dpi=150)
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
