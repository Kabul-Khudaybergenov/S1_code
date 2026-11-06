"""Format the scenario tables (profile table, Table A1, Table A2) from data/scenario.json and the operator output.

Formatting only: values are copied from the scenario file and from the operator output used for Figure 4.
"""
import os

from config import TABLES
from scenario_ops import CHARS, write_summary
FORM = {"OPEN": "Open", "QA": "Q\\&A", "PRES": "Pres.", "IND": "Indiv.", "GRP": "Group", "DISC": "Disc.",
        "CLOSE": "Close"}
NAMES = {"C1": "C1 Discipline and organisation", "C2": "C2 Attention and engagement",
         "C3": "C3 Socio-emotional climate", "C4": "C4 Interaction and cognitive activation"}


def num(x, nd=1):
    if x is None:
        return "?"
    if x == "na":
        return "--"
    if isinstance(x, float) and not x.is_integer():
        return f"{x:.{nd}f}"
    return f"{int(x)}"


def signed(x):
    if x in (None, "na"):
        return num(x)
    return f"+{x}" if x > 0 else (f"$-${abs(x)}" if x < 0 else "0")


def segs(lst):
    return ", ".join(str(x) for x in lst) if lst else "--"


def rng(a, b):
    a_s = "--" if a is None else num(a)
    if b is None:
        return f"$\\geq${a_s}"
    if a == b:
        return num(a)
    return f"{a_s}--{num(b)}"


def flagtext(o):
    parts = []
    for key, lab in (("Z", "Z"), ("J", "J"), ("E", "E"), ("na", "n/a"), ("ne", "n/e")):
        if o[key]:
            parts.append(f"{lab}: {segs(o[key])}")
    return "; ".join(parts) if parts else "--"


def table_profile(sc, out):
    rows = []
    for c in CHARS:
        o = out[c]
        rows.append(f"{NAMES[c]} & {o['n_estimable']} & {o['mean']:.2f} & {o['min']:.2f} ({o['argmin']}) & "
                    f"{o['sd_population']:.2f} & {segs(o['jumps'])} & {flagtext(o)} \\\\")
    m = sc["management"]
    mrow = ("C5 Pedagogical management ($M$) & \\multicolumn{6}{m{0.72\\fulllength}}{\\raggedright "
            f"Goal clarity {m['M5.1']['values'][0]}/2; group task {signed(m['M5.2']['values'][5])}\\% over the plan "
            f"and consolidation {signed(m['M5.2']['values'][7])}\\% (expected $\\pm$15\\%); responsiveness latency "
            f"{m['M5.3']['values'][5]}~s in segment 6 (expected $\\leq${m['M5.3']['target'][1]}~s); task setting "
            f"{m['M5.4']['values'][5]}/2 at the start of group work}} \\\\")
    rho = out["covariation_spearman"]
    rtxt = "; ".join(f"{k.replace('-', '--')}: {v['rho']:.2f}".replace(": -", ": $-$")
                     for k, v in rho.items() if v["rho"] is not None)
    body = "\n".join(rows + ["\\midrule", mrow])
    p = out["parameters"]
    tex = r"""\begin{table}[H]
\caption{Diagnostic profile $Q$ of the constructed lesson scenario produced by Equations~(5)--(10) ($\theta = """ + \
        f"{p['theta']}" + r"""$, $\lambda = """ + f"{p['lambda']}" + r"""$, $\varepsilon = """ + f"{p['epsilon']}" + \
        r"""$, $\kappa = """ + f"{p['kappa']}" + r"""$, $\delta = """ + f"{p['delta']}" + r"""$, equal weights). Values are conformity estimates on a 0--1 scale.\label{tab:profile}}
\begin{adjustwidth}{-\extralength}{0cm}
\small
\begin{tabularx}{\fulllength}{>{\raggedright\arraybackslash}m{0.22\fulllength}>{\centering\arraybackslash}m{0.08\fulllength}>{\centering\arraybackslash}m{0.07\fulllength}>{\centering\arraybackslash}m{0.1\fulllength}>{\centering\arraybackslash}m{0.08\fulllength}>{\centering\arraybackslash}m{0.07\fulllength}>{\raggedright\arraybackslash}X}
\toprule
\textbf{Characteristic} & \textbf{Estimable segments} & \textbf{Mean} & \textbf{Minimum (segment)} & \textbf{SD (population)} & \textbf{Jumps} & \textbf{Flags (segments)} \\
\midrule
""" + body + r"""
\bottomrule
\end{tabularx}
\end{adjustwidth}
\noindent{\footnotesize{Z = problem zone; J = referred to the teacher's professional judgement; E = critical event; jumps are segments $t$ with $|\hat{L}_j(t) - \hat{L}_j(t')| > \delta$, where $t'$ is the preceding estimable segment. Descriptive co-variation across the nine segments (Spearman $\rho$): """ + rtxt + \
        r""". With nine segments and many estimates at the ceiling of 1.00, these coefficients are unstable and partly reflect overlapping indicators; they are reported only to show the form of the output.}}
\end{table}
"""
    with open(os.path.join(TABLES, "tab_profile.tex"), "w", encoding="utf-8") as f:
        f.write(tex)


def table_A1(sc):
    forms = [s["form"] for s in sc["segments"]]
    head = " & ".join(f"\\textbf{{{s['t']}}}" for s in sc["segments"])
    sub = " & ".join(FORM[f] for f in forms)
    lines, cur = [], None
    for k, v in sc["indicators"].items():
        if v["char"] != cur:
            if cur is not None:
                lines.append("\\midrule")
            cur = v["char"]
        tg = v["target"]
        parts = []
        if "default" in tg:
            parts.append(rng(*tg["default"]))
        parts += [f"{FORM[f]} {rng(*ab)}" for f, ab in tg.items() if f != "default"]
        vals = " & ".join(num(x) for x in v["values"])
        crit = "$^{\\dagger}$" if k in sc["_meta"].get("critical_indicators", []) else ""
        unit = v["unit"].replace("-", "--")
        lines.append(f"{k} {v['name']}{crit} ({unit}) & {'; '.join(parts)} & {num(v['w'])} & {vals} \\\\")
    lines.append("\\midrule")
    for k, v in sc["management"].items():
        vals = " & ".join(signed(x) if k == "M5.2" else num(x) for x in v["values"])
        lo, hi = v["target"]
        tg = (f"$\\pm${hi}" if lo == -hi else rng(lo, hi))
        unit = v["unit"].replace("-", "--")
        lines.append(f"{k} {v['name']} ({unit}) & {tg} & -- & {vals} \\\\")
    body = "\n".join(lines).replace("%", "\\%")
    tex = r"""\begin{table}[H]
\caption{Indicator values of the constructed lesson scenario (grade 8 mathematics, 45 min, $T = 9$ segments of 5 min) with the context-conditioned target ranges $[a_k(c), b_k(c)]$ and tolerances $w_k$ used in Equation~(5). Values, ranges and tolerances were set by the authors for illustration; they are neither observational data nor recommended norms.\label{tab:A1}}
\begin{adjustwidth}{-\extralength}{0cm}
\scriptsize
\setlength{\tabcolsep}{3pt}
\begin{tabularx}{\fulllength}{>{\raggedright\arraybackslash}m{0.25\fulllength}>{\raggedright\arraybackslash}X c ccccccccc}
\toprule
\textbf{Indicator (unit)} & \textbf{Target range by activity form} & $\boldsymbol{w_k}$ & """ + head + r""" \\
 & & & """ + sub + r""" \\
\midrule
""" + body + r"""
\bottomrule
\end{tabularx}
\end{adjustwidth}
\noindent{\footnotesize{Activity forms: Open = organisation; Q\&A = whole-class questioning; Pres. = teacher presentation; Indiv. = individual work; Group = group work; Disc. = whole-class discussion; Close = closing. A range without a form label applies to all forms without their own range. ``--'' = not applicable in that segment (e.g., no transition or no student error occurred); ``?'' = applicable but not observable with whole-class recording. $^{\dagger}$ Critical indicator: any value outside its range raises an event flag E. Management indicators are compared with their own expected ranges and are not aggregated into an estimate.}}
\end{table}
"""
    with open(os.path.join(TABLES, "tabA1_scenario.tex"), "w", encoding="utf-8") as f:
        f.write(tex)


def table_A2(out):
    rows = []
    for r in out["sensitivity"]["one_at_a_time"]:
        f = r["flags"]
        cells = []
        for c in CHARS:
            parts = []
            if f[c]["Z"]:
                parts.append("Z " + segs(f[c]["Z"]))
            if f[c]["J"]:
                parts.append("J " + segs(f[c]["J"]))
            cells.append("; ".join(parts) if parts else "--")
        label = r["setting"].replace("baseline", "Baseline").replace("theta", "$\\theta$").replace("lambda", "$\\lambda$").replace(
            "epsilon", "$\\varepsilon$").replace("kappa", "$\\kappa$")
        rows.append(f"{label} & " + " & ".join(cells) + " \\\\")
    sp = out["sensitivity"]
    pers = sp["segment6_persistence"]
    tex = r"""\begin{table}[H]
\caption{Sensitivity of the profile flags to the parameters of Equations~(7) and (9), varied one at a time around the baseline. Event flags E (C3, segments 4 and 6) do not depend on these parameters.\label{tab:A2}}
\begin{adjustwidth}{-\extralength}{0cm}
\small
\begin{tabularx}{\fulllength}{>{\raggedright\arraybackslash}m{0.16\fulllength}>{\raggedright\arraybackslash}X>{\raggedright\arraybackslash}X>{\raggedright\arraybackslash}X>{\raggedright\arraybackslash}X}
\toprule
\textbf{Setting} & \textbf{C1} & \textbf{C2} & \textbf{C3} & \textbf{C4} \\
\midrule
""" + "\n".join(rows) + r"""
\bottomrule
\end{tabularx}
\end{adjustwidth}
\noindent{\footnotesize{Baseline: $\theta = 0.6$, $\lambda = 0.3$, $\varepsilon = 0.15$, $\kappa = 0.5$. Over the full grid of """ + \
        f"{sp['grid_size']}" + r""" combinations of $\theta \in \{0.5, 0.6, 0.7\}$, $\lambda \in \{0.2, 0.3, 0.4\}$ and $\varepsilon \in \{0.10, 0.15, 0.20\}$, segment 6 was flagged (Z or J) for C1 in """ + \
        f"{pers['any_flag_C1']}" + r""" and for C2 in """ + f"{pers['any_flag_C2']}" + r""" combinations, and flagged as a problem zone (Z) in """ + \
        f"{pers['C1']}" + r""" and """ + f"{pers['C2']}" + r""" combinations, respectively.}}
\end{table}
"""
    with open(os.path.join(TABLES, "tabA2_sensitivity.tex"), "w", encoding="utf-8") as f:
        f.write(tex)


def main():
    sc, _, _, out = write_summary()
    table_profile(sc, out)
    table_A1(sc)
    table_A2(out)
    for old in ("tab5_profile.tex",):
        p = os.path.join(TABLES, old)
        if os.path.exists(p):
            os.remove(p)
    print("wrote tab_profile.tex, tabA1_scenario.tex, tabA2_sensitivity.tex")


if __name__ == "__main__":
    main()
