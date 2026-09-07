# The Ozhand Chart

A candlestick-inspired visualization for comparing per-capita national income
growth and income distribution across countries over time. Concept, design,
and analysis by **Ozhand** (b.Ozhand96@gmail.com). See `MANUSCRIPT.md` for the
full write-up (motivation, related work, method, worked example).

## What it shows

For each country and year: a "tube" whose floor and ceiling are the average
income of the bottom and top income deciles, with a thick midline for the
mean, on a log-scale y-axis. Tube width is a visual proxy for inequality.

## Data sources (real, cited)

- **Mean income**: GDP per capita, PPP (current international $) — World Bank.
- **Top-decile income share** (before tax): World Inequality Database
  (WID.world), via Our World in Data's grapher CSV endpoint.
- **Gini coefficient** (before tax): World Inequality Database (WID.world),
  via the same OWID endpoint — included as an independent check on the
  inequality reading (see manuscript Section 4).
- **Bottom-decile income share**: currently an **approximate, roughly
  time-invariant estimate** per country, not a real annual series — the
  clearest open item for improving this project (see Limitations below).

Full citations are listed at the bottom of `MANUSCRIPT.md`.

## Reproducing the chart

```bash
pip install -r requirements.txt

# Optional: refetch live data from World Bank / OWID and compare
# against the snapshot used in the manuscript
python src/fetch_data.py

# Render the chart from the committed snapshot data
python src/plot_chart.py
```

This writes `ozhand_chart.png`. An interactive HTML/JS version (click a
node to see the exact year's numbers) is in `interactive/ozhand-chart.html`.

## Limitations

- Bottom-of-distribution data: Germany's tube floor now uses the real WID
  "poorest 50%" income-share series (fully real, annual, cited). USA and UK
  still use an approximate, roughly time-invariant bottom-decile estimate —
  `fetch_data.py` already knows how to pull their real WID poorest-50% series
  too; it just needs to be run somewhere without the request-size limits this
  session's fetch tool hit on the full WID CSV. Run `python src/fetch_data.py`
  and it will fetch all three countries' real data directly.
- Japan is excluded: WID's coverage for Japan in 1990–2024 is too sparse
  (effectively one usable data point) to support the method with real data.

## License

MIT for the code in this repository. The underlying data remains subject to
its original sources' terms (World Bank Open Data license; WID.world /
Our World in Data — see their respective citation and reuse pages).

## Citing this chart

If you use or reference the Ozhand Chart, please credit:
Ozhand (b.Ozhand96@gmail.com), "The Ozhand Chart: A Candlestick-Inspired
Visualization for Cross-Country Income Growth and Distribution."
