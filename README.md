# Supplementary File S1 — scripts and constructed scenario

Code accompanying the manuscript

> Urakov, S. R., Marakhimov, A. A., Khudaybergenov, K. K., & Ergasheva, D. A.
> *From Observable Classroom Features to Uncertainty-Aware Diagnostic Profiles: A Diagnostic–Regulatory
> Model of Lesson Delivery Quality for Technology-Supported Observation.* Submitted to *Education Sciences* (MDPI), 2026.

## Contents

| File | Purpose |
|---|---|
| `scenario_ops.py` | Transparent instantiation of operators F2–F4: conformity scores (Eq. 5), estimates and coverage (Eq. 6), uncertainty (Eq. 7), dynamics (Eq. 8), flags Z/J/E and management notes (Eq. 9), profile (Eq. 10), the fixed-norm counterfactual of Section 4.5 and the sensitivity grid of Table A2. Writes `data/scenario_summary.json`. |
| `data/scenario.json` | The constructed lesson: segments, activity forms, indicator values, context-conditioned target ranges `[a_k(c), b_k(c)]`, tolerances `w_k`, management indicators and the parameters θ, λ, ε, κ, δ. |
| `data/scenario_summary.json` | Output of `scenario_ops.py` (estimates, uncertainties, coverage, flags, dynamics, co-variation, counterfactual, sensitivity). |
| `make_tables.py` | Formats Table 6 (profile), Table A1 (scenario) and Table A2 (sensitivity) as LaTeX from the files above. |
| `fig_1_conceptual.py` … `fig_4_profile.py` | Draw Figures 1–4. |
| `make_all.py` | Draws all four figures. |
| `config.py`, `diagram.py` | Shared plotting settings (MDPI layout, Okabe–Ito palette, PNG export at 600 dpi) and small drawing helpers. |

Value codes in `scenario.json`: a number = observed; `null` = applicable but not observable with
whole-class recording; `"na"` = not applicable in that segment. A target range that every value would
satisfy is not used; such an indicator is coded `"na"` instead (see Section 4.3 of the manuscript).

## Reproducing the figures and tables

Requires Python 3.10 or later.

```bash
pip install -r requirements.txt
python make_all.py      # Figures 1-4  -> output/figures/*.png (600 dpi, RGB, white background)
python make_tables.py   # Tables 6, A1, A2 -> output/tables/*.tex; also refreshes data/scenario_summary.json
python scenario_ops.py  # prints the profile, flags, counterfactual and sensitivity results to the console
```

When the folder sits next to the manuscript sources (`../article/`), the outputs are written there
instead of to `output/`.

The figures use the Arial font if it is installed; otherwise matplotlib falls back to DejaVu Sans, which
changes the appearance but not the content.

## Checking the numbers in the manuscript

`python scenario_ops.py` prints, for C1–C4, the segment-level estimates `L`, uncertainties `u`,
coverage, flags (Z, J, E), jumps, mean, minimum and its segment; then the Spearman co-variation,
the management notes, the fixed-norm counterfactual for student talk share (Section 4.5) and the
sensitivity analysis (27-point grid and one-at-a-time rows of Table A2). These are the values quoted
in Section 4.5, Table 6, Figure 4 and Table A2.

## Licence and citation

The code is released under the MIT Licence (see `LICENSE`). If you use it, please cite the manuscript
above; a `CITATION.cff` file is included.
