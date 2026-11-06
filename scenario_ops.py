"""Transparent instantiation of operators F2-F4 (Equations 5-10) applied to the constructed scenario.

Used only to draw Figure 4 and to format the scenario tables (Table 6, Tables A1-A2); no empirical analysis.

Value codes in scenario.json: number = observed; null = applicable but not observed; "na" = not applicable.
"""
import copy
import itertools
import json
import math
import os

from config import DATA

CHARS = ["C1", "C2", "C3", "C4"]


def load():
    with open(os.path.join(DATA, "scenario.json"), encoding="utf-8") as f:
        return json.load(f)


def target_for(ind, form):
    tg = ind["target"]
    return tg.get(form, tg.get("default", [None, None]))


def conformity(p, a, b, w):
    """Eq. (5): 1 inside [a, b] (b = +inf for one-sided ranges); linear decrease over tolerance w outside it."""
    if p is None or p == "na":
        return None
    lo = -math.inf if a is None else a
    hi = math.inf if b is None else b
    if lo <= p <= hi:
        return 1.0
    d = lo - p if p < lo else p - hi
    return max(0.0, 1.0 - d / w)


def ranks(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(xs):
        j = i
        while j + 1 < len(xs) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return r


def spearman(x, y):
    rx, ry = ranks(x), ranks(y)
    mx, my = sum(rx) / len(rx), sum(ry) / len(ry)
    sxy = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    sx = math.sqrt(sum((a - mx) ** 2 for a in rx))
    sy = math.sqrt(sum((b - my) ** 2 for b in ry))
    return None if sx == 0 or sy == 0 else sxy / (sx * sy)


def run(sc=None, par=None):
    sc = sc or load()
    par = dict(sc["_meta"]["parameters"], **(par or {}))
    theta, lam, eps, kappa, delta = par["theta"], par["lambda"], par["epsilon"], par["kappa"], par["delta"]
    critical = set(sc["_meta"].get("critical_indicators", []))
    forms = [s["form"] for s in sc["segments"]]
    T = len(forms)
    ind = sc["indicators"]
    s = {k: [conformity(v["values"][t], *target_for(v, forms[t]), v["w"]) for t in range(T)] for k, v in ind.items()}
    est = {}
    for c in CHARS:
        keys = [k for k, v in ind.items() if v["char"] == c]
        out = {k: [] for k in ("L", "u", "cov", "Z", "J", "E", "status")}
        for t in range(T):
            applicable = [k for k in keys if ind[k]["values"][t] != "na"]
            avail = [k for k in applicable if ind[k]["values"][t] is not None]
            ev = any(k in critical and s[k][t] is not None and s[k][t] < 1 for k in avail)
            out["E"].append(ev)
            if not applicable or not avail:
                out["L"].append(None), out["u"].append(None), out["cov"].append(None)
                out["Z"].append(False), out["J"].append(False)
                out["status"].append("n/a" if not applicable else "n/e")
                continue
            vals = [s[k][t] for k in avail]
            m = sum(vals) / len(vals)
            var = sum((x - m) ** 2 for x in vals) / len(vals)
            cov = len(avail) / len(applicable)
            u = math.sqrt((var + eps ** 2) / len(vals)) + lam * (1 - cov)  # Eq. (7); var = v_j(t), population
            z = (m + u < theta) and cov >= kappa
            crit_unobs = any(k in critical for k in applicable if k not in avail)
            j = (not z) and (m - u < theta or cov < kappa or crit_unobs)
            out["L"].append(m), out["u"].append(u), out["cov"].append(cov)
            out["Z"].append(z), out["J"].append(j), out["status"].append("ok")
        idx = [t for t in range(T) if out["L"][t] is not None]
        av = [out["L"][t] for t in idx]
        jumps = [idx[i] + 1 for i in range(1, len(idx)) if abs(out["L"][idx[i]] - out["L"][idx[i - 1]]) > delta]
        mean = sum(av) / len(av)
        out.update({"mean": mean, "min": min(av), "argmin": out["L"].index(min(av)) + 1,
                    "sd": math.sqrt(sum((x - mean) ** 2 for x in av) / len(av)), "jumps": jumps,
                    "n_estimable": len(av)})
        est[c] = out
    rho = {}
    for a, b in itertools.combinations(CHARS, 2):
        ts = [t for t in range(T) if est[a]["L"][t] is not None and est[b]["L"][t] is not None]
        r = spearman([est[a]["L"][t] for t in ts], [est[b]["L"][t] for t in ts])
        rho[f"{a}-{b}"] = {"rho": None if r is None else round(r, 2), "n": len(ts)}
    notes = []
    for k, v in sc["management"].items():
        lo, hi = v["target"]
        for t, x in enumerate(v["values"]):
            if x not in (None, "na") and not (lo <= x <= hi):
                notes.append({"indicator": k, "segment": t + 1, "value": x})
    return sc, s, est, rho, notes


def flags(est):
    return {c: {"Z": [t + 1 for t, v in enumerate(e["Z"]) if v], "J": [t + 1 for t, v in enumerate(e["J"]) if v],
                "E": [t + 1 for t, v in enumerate(e["E"]) if v],
                "na": [t + 1 for t, v in enumerate(e["status"]) if v == "n/a"],
                "ne": [t + 1 for t, v in enumerate(e["status"]) if v == "n/e"]} for c, e in est.items()}


def sensitivity(sc):
    base = sc["_meta"]["parameters"]
    one_at_a_time = [("baseline", {})]
    for name, vals in (("theta", (0.5, 0.7)), ("lambda", (0.2, 0.4)), ("epsilon", (0.10, 0.20)),
                       ("kappa", (0.34, 0.67))):
        for v in vals:
            one_at_a_time.append((f"{name} = {v}", {name: v}))
    rows = []
    for label, p in one_at_a_time:
        _, _, e, _, _ = run(copy.deepcopy(sc), p)
        f = flags(e)
        rows.append({"setting": label, "flags": f})
    grid = list(itertools.product((0.5, 0.6, 0.7), (0.2, 0.3, 0.4), (0.10, 0.15, 0.20)))
    persist = {"C1": 0, "C2": 0, "any_flag_C1": 0, "any_flag_C2": 0}
    for th, la, ep in grid:
        _, _, e, _, _ = run(copy.deepcopy(sc), {"theta": th, "lambda": la, "epsilon": ep})
        for c in ("C1", "C2"):
            persist[c] += int(e[c]["Z"][5])
            persist[f"any_flag_{c}"] += int(e[c]["Z"][5] or e[c]["J"][5])
    return rows, persist, len(grid), base


def summary(sc=None):
    sc = sc or load()
    sc, s, est, rho, notes = run(sc)
    out = {"parameters": sc["_meta"]["parameters"]}
    for c, e in est.items():
        out[c] = {"mean": round(e["mean"], 2), "min": round(e["min"], 2), "argmin": e["argmin"],
                  "sd_population": round(e["sd"], 2), "jumps": e["jumps"], "n_estimable": e["n_estimable"],
                  "L": [None if x is None else round(x, 2) for x in e["L"]],
                  "u": [None if x is None else round(x, 2) for x in e["u"]],
                  "coverage": [None if x is None else round(x, 2) for x in e["cov"]],
                  "status": e["status"]}
        out[c].update(flags({c: e})[c])
    out["covariation_spearman"] = rho
    out["management_notes"] = notes
    cf = copy.deepcopy(sc)
    cf["indicators"]["P4.4"]["target"] = {"default": [5, 35]}
    _, s_cf, est_cf, _, _ = run(cf)
    out["fixed_norm_counterfactual"] = {
        "P4.4_conformity": [None if x is None else round(x, 2) for x in s_cf["P4.4"]],
        "C4_L": [None if x is None else round(x, 2) for x in est_cf["C4"]["L"]],
        "C4_u": [None if x is None else round(x, 2) for x in est_cf["C4"]["u"]],
        "C4_flags": flags({"C4": est_cf["C4"]})["C4"]}
    rows, persist, n, _ = sensitivity(sc)
    out["sensitivity"] = {"one_at_a_time": rows, "grid_size": n, "segment6_persistence": persist}
    return sc, s, est, out


def write_summary(path=None):
    sc, s, est, out = summary()
    path = path or os.path.join(DATA, "scenario_summary.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
    return sc, s, est, out


if __name__ == "__main__":
    _, _, _, o = write_summary()
    print(json.dumps({c: {k: o[c][k] for k in ("L", "u", "coverage", "Z", "J", "E", "na", "ne", "jumps", "mean",
                                              "min", "argmin")} for c in CHARS}, indent=None))
    print(o["covariation_spearman"])
    print(o["management_notes"])
    print(o["fixed_norm_counterfactual"])
    print(o["sensitivity"]["segment6_persistence"], o["sensitivity"]["grid_size"])
    for r in o["sensitivity"]["one_at_a_time"]:
        print(r["setting"], {c: (v["Z"], v["J"]) for c, v in r["flags"].items()})
