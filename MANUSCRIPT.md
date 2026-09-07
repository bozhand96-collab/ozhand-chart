# The Ozhand Chart: A Candlestick-Inspired Visualization for Cross-Country Income Growth and Distribution

**Author:** Ozhand (b.Ozhand96@gmail.com)

## Abstract

Standard per-capita income figures (e.g. GDP per capita) summarize a country's average material standard of living but conceal how that average is distributed across the population. This paper introduces the **Ozhand Chart**, a visualization that plots per-capita national income over time for one or more countries as a 3D "tube" whose floor and ceiling correspond to the average income of the bottom and top income deciles, with a thick midline for the mean, rendered on a logarithmic vertical axis. Tube width serves as a direct visual proxy for income inequality, conceptually analogous to the Gini coefficient, so a single chart lets a reader see simultaneously whether per-capita income is growing and whether that growth is broadly or narrowly shared. We situate the design relative to existing statistical graphics — box plots, financial candlestick charts, central-bank fan charts, and decile-based bubble charts — and demonstrate the method with real World Bank and World Inequality Database (WID) data for the United States, Germany, the United Kingdom, and Japan, 1990–2024.

## 1. Motivation

A country's GDP per capita is the most widely cited single-number summary of economic progress, and it is routinely used in political and media discourse as a proxy for "how well off people are." This use is misleading whenever growth is unevenly distributed: a rising mean is consistent with either broadly shared gains or with gains concentrated at the top of the distribution while median incomes stagnate. Analysts typically address this by plotting a second, separate series — a Gini coefficient or a top-decile income-share line — alongside the per-capita income line. This forces the reader to mentally fuse two charts to answer a single, simple question: *did the average person's income grow along with the national average, or did most of the gain go to a narrow group at the top?* The Ozhand Chart is designed to answer that question in a single glance, in a single chart, for a single country or for several countries compared side by side.

## 2. Related work

The Ozhand Chart draws on four existing graphical idioms, none of which individually addresses the problem above:

- **Box plots** encode a distribution's spread and central tendency in one mark, but are typically drawn per time-point as discrete, unconnected boxes, and are rarely used with a logarithmic axis for cross-country income comparison.
- **Financial candlestick charts** use a body-and-wick idiom to show a price range around an open/close pair over discrete time intervals — an idiom that maps naturally onto "income range around a mean" but has, to our knowledge, not been applied to national income-distribution data.
- **Fan charts**, most famously the Bank of England's inflation fan chart, show a widening band of uncertainty around a central projection over time. The Ozhand Chart borrows the "band around a midline" visual grammar, but the band here encodes an empirically observed distribution (decile spread), not forecast uncertainty.
- **Decile-based bubble/scatter charts**, such as those produced by Reuters for income deciles over time, show the same underlying decile data but as discrete points rather than as a continuous, comparably-scaled band across countries.

The contribution of the Ozhand Chart is the specific combination of these idioms — a candlestick-style range-and-midline mark, drawn continuously over time, on a logarithmic axis, with band width used explicitly as a Gini-like inequality proxy, and multiple countries overlaid on one shared coordinate system. Each individual element has precedent; the combination and its explicit reading as "growth vs. distribution in one view" is, to the best of the author's knowledge, new.

## 3. Method

For a country in year *t*:

- **Midline** *m(t)* = per-capita national income (GDP per capita, PPP-adjusted, current international $), sourced from the World Bank.
- **Ceiling** *h(t)* = average income of the top income decile = *s₁₀(t) × 10 × m(t)*, where *s₁₀(t)* is the top decile's share of national income in year *t* (World Inequality Database, pre-tax national income, before-tax series).
- **Floor** *l(t)* = average income of the bottom of the distribution. Where available (Germany), this uses the real, cited WID "poorest 50%" income share, giving *l(t) = s₅₀(t) × 2 × m(t)*; otherwise (USA, UK) it uses an approximate, roughly time-invariant bottom-decile share as a placeholder pending a full WID pull (see Section 5).
- The vertical axis uses a log₁₀ scale so that countries or periods spanning very different absolute income levels remain visually comparable on one chart.
- Tube width at time *t*, *h(t) − l(t)* (or the ratio *h(t)/l(t)* on the log scale), increases monotonically with standard inequality measures and can be read as a visual proxy for the Gini coefficient without computing it explicitly.

**A visualization caveat worth stating plainly.** On a log axis, the ceiling and floor can appear roughly equidistant from the midline even when the underlying dollar gaps are highly asymmetric — because the log scale compresses large values. For the US in 2024, the ceiling sits about 4.7× the mean and the floor about 1/5.3 of the mean; those ratios place the two lines at visually similar log-distances from the midline, but in dollar terms the gap from mean to ceiling (~$315,000) is roughly 4.5× the gap from floor to mean (~$70,000). The log-scale chart is the right tool for comparing countries at very different income levels, but it should not be read as showing the dollar-symmetry of the distribution. We therefore pair every log-scale panel with a linear-scale panel showing the same data in true dollar proportions (Figure, Section 4), and recommend any future presentation of the Ozhand Chart do the same rather than rely on the log-scale version alone.

Reading the chart: a tube that rises while staying narrow indicates broadly shared income growth; a tube that rises while widening indicates growth concentrated toward the top decile; a flat midline with a narrowing tube (observed for Iran in the author's earlier four-country pilot) indicates broad-based stagnation rather than redistribution.

## 4. Illustrative example: USA, Germany, UK, 1990–2024

Using World Bank GDP-per-capita PPP series and two independent real WID series — the top-decile income share (`income-share-top-10-before-tax-wid`) and the Gini coefficient (`gini-coefficient-wid`), both before-tax, both annual — three country-level Ozhand Charts were produced for 1990, 2010, 2020, and 2024 (an interactive version is available at [insert repository/demo link]). The Gini series lets us cross-validate the tube-width reading against a standard, independently computed inequality measure rather than relying on tube width alone.

| Country | Mean income growth, 1990→2024 | Top-decile share | Gini coefficient (before tax) |
|---|---|---|---|
| United States | 23,889 → 85,810 (~3.6×) | 38.8% → 46.8% | 0.513 → 0.587 |
| Germany | 42,355 → 62,830 (~1.5×) | 32.6% → 37.6% (2022) | 0.437 → 0.490 (2022) |
| United Kingdom | 16,505 → 62,009 (~3.8×) | 32.9% → 36.0% (2021) | 0.460 → 0.468 (2021) |

All three countries show rising Gini coefficients over the period, confirming the tube-widening pattern independently of the top-decile-share construction. The US shows both the largest proportional income growth and the largest absolute Gini increase (+0.074), consistent with the reading that its growth has been the least evenly distributed of the three. The UK's Gini barely moves (+0.008) despite the second-largest income growth, suggesting its growth has been comparatively more evenly distributed than the top-decile share alone might imply — a useful check that the two inequality measures do not always tell exactly the same story and both should be reported.

**Citations for the reused data:**
- World Bank, GDP per capita, PPP (current international $).
- World Inequality Database (WID.world) (2026) – with major processing by Our World in Data. "Income share of the top 10% (before tax) – WID" [dataset].
- World Inequality Database (WID.world) (2026) – with major processing by Our World in Data. "Gini coefficient (before tax) – WID" [dataset].

## 5. Limitations and required work before submission

This draft is not yet ready for journal submission. Both the top-decile share and the Gini coefficient used above are real, annual, directly citable WID series, which substantially strengthens the worked example. The following gaps should still be closed:

1. **Bottom-decile time series.** The tube's floor line still uses a single, roughly time-invariant bottom-decile share estimate per country rather than an annual series, because a fully reliable free WID time series for `p0p10` was not obtained during this exploratory phase. A rigorous version needs the WID bulk API queried per country per year for the `p0p10` income share. Since the Gini coefficient is now included as an independent, fully real check on the inequality reading (Section 4), this limitation affects only the visual floor of the tube, not the paper's substantive inequality claims.
2. **Reproducible, open code.** Reviewers and readers should be able to regenerate the chart from raw data. A public repository (GitHub) with the data-processing script and rendering code should accompany submission.
3. **Honest novelty framing.** The related-work section above must be expanded with proper citations (Tukey for box plots, Bank of England fan chart documentation, Reuters' decile bubble chart piece, and any other prior "candlestick for economic data" attempts found in a fuller literature search) so reviewers see the author is aware of, and explicitly building on, prior art rather than claiming an unprecedented invention.
4. **Scope note.** Japan was excluded from this draft's worked example because WID's income-share series for Japan is too sparse (effectively one usable data point in 1990–2024) to support either the top-decile-share or Gini components of the method with real annual data.

## 6. Candidate venues

In order of estimated fit and acceptance likelihood: *Journal of Data Science, Statistics and Visualisation* (JDSSV) as the primary target; *Nightingale* (Data Visualization Society magazine) as a faster, lower-barrier venue for initial visibility and feedback; *Significance* (RSS/ASA) as a secondary option. Traditional empirical economics journals (AER, QJE, JEP) are not appropriate venues, since the contribution is a visualization method rather than an empirical economic finding.

---
*Concept, design, and analysis by Ozhand (b.Ozhand96@gmail.com). Draft prepared with research assistance from Claude (Anthropic).*
