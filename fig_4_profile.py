"""Figure 4: diagnostic profile of the constructed lesson scenario (operators of Equations 5-10)."""
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from config import BLUE, CM, FILL_LIGHT, FULL_W, GRID, INK, INK2, MUTED, SERIES, VERMILION, save
from scenario_ops import target_for, write_summary

FORM_LABEL = {"OPEN": "Open", "QA": "Q&A", "PRES": "Pres.", "IND": "Indiv.", "GRP": "Group",
              "DISC": "Disc.", "CLOSE": "Close"}
CHAR_LABEL = {"C1": "C1 Organisation", "C2": "C2 Engagement", "C3": "C3 Climate", "C4": "C4 Interaction"}


def num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def band_steps(ax, ind, forms, ymax):
    for t, f in enumerate(forms):
        if not num(ind["values"][t]):
            continue
        a, b = target_for(ind, f)
        a = 0 if a is None else a
        b = ymax if b is None else b
        ax.add_patch(Rectangle((t + 0.55, a), 0.9, b - a, facecolor="#E3EEF7", edgecolor="none", zorder=0))


def runs(ts, ys):
    """Split a series into runs of consecutive defined segments (no line across undefined segments)."""
    out, cur = [], []
    for t, y in zip(ts, ys):
        if y is None:
            if cur:
                out.append(cur)
            cur = []
        else:
            if cur and t != cur[-1][0] + 1:
                out.append(cur)
                cur = []
            cur.append((t, y))
    if cur:
        out.append(cur)
    return out


def style(ax):
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.grid(axis="y", color=GRID, linewidth=0.4)
    ax.set_axisbelow(True)


def main():
    sc, s, est, summ = write_summary()
    forms = [x["form"] for x in sc["segments"]]
    T = len(forms)
    ts = list(range(1, T + 1))
    xt = [f"{t}\n{FORM_LABEL[f]}" for t, f in zip(ts, forms)]
    ind = sc["indicators"]
    theta = sc["_meta"]["parameters"]["theta"]

    fig = plt.figure(figsize=(FULL_W, 15.6 * CM))
    gs = fig.add_gridspec(3, 3, height_ratios=[1.0, 1.25, 1.15], hspace=0.66, wspace=0.34)

    specs = [("P2.1", "(a) P2.1 On-task share (%)", 100),
             ("P4.4", "(b) P4.4 Student talk share (%)", 100),
             ("P1.2", "(c) P1.2 Disruption time share (%)", 40)]
    for i, (k, title, ymax) in enumerate(specs):
        ax = fig.add_subplot(gs[0, i])
        v = ind[k]
        band_steps(ax, v, forms, ymax)
        ys = [y if num(y) else None for y in v["values"]]
        for r in runs(ts, ys):
            ax.plot([p[0] for p in r], [p[1] for p in r], color=INK2, linewidth=1.0, zorder=2)
        pts = [(t, y) for t, y in zip(ts, ys) if y is not None]
        ax.plot([p[0] for p in pts], [p[1] for p in pts], "o", color=BLUE, markersize=4.4,
                markeredgecolor="white", markeredgewidth=0.6, zorder=3)
        if k == "P4.4":
            ax.axhline(35, color=MUTED, linewidth=0.9, linestyle=(0, (2, 2)), zorder=1)
        ax.set_xlim(0.5, T + 0.5)
        ax.set_ylim(0, ymax)
        ax.set_xticks(ts)
        ax.set_xticklabels([str(t) for t in ts])
        ax.set_title(title, loc="left", fontsize=7.6, color=INK, pad=4)
        style(ax)
        if i == 0:
            ax.set_ylabel("Indicator value")
        ax.set_xlabel("Segment")

    ax = fig.add_subplot(gs[1, :])
    offs = {"C1": -0.18, "C2": -0.06, "C3": 0.06, "C4": 0.18}
    for c, e in est.items():
        col, mk, ls = SERIES[c]
        for r in runs(ts, e["L"]):
            xs = [p[0] + offs[c] for p in r]
            ax.plot(xs, [p[1] for p in r], linestyle=ls, color=col, linewidth=1.2, zorder=3)
        xs = [t + offs[c] for t, y in zip(ts, e["L"]) if y is not None]
        ys = [y for y in e["L"] if y is not None]
        us = [u for u in e["u"] if u is not None]
        ax.errorbar(xs, ys, yerr=[[min(y, u) for y, u in zip(ys, us)], [min(1 - y, u) for y, u in zip(ys, us)]],
                    fmt="none", ecolor=col, elinewidth=0.9, capsize=1.6, alpha=0.8, zorder=2)
        ax.plot(xs, ys, linestyle="none", marker=mk, color=col, markersize=4.4, markeredgecolor="white",
                markeredgewidth=0.6, label=CHAR_LABEL[c], zorder=4)
    ax.axhline(theta, color=INK2, linewidth=0.8, linestyle=(0, (4, 2)))
    ax.text(0.58, theta - 0.02, r"threshold $\theta$", fontsize=7, color=INK2, va="top")
    ax.set_xlim(0.5, T + 0.5)
    ax.set_ylim(0.0, 1.05)
    ax.set_xticks(ts)
    ax.set_xticklabels(xt)
    ax.set_ylabel(r"$\hat{L}_j(t) \pm u_j(t)$")
    ax.set_title("(d) Conformity estimates with uncertainty", loc="left", fontsize=7.6, color=INK, pad=4)
    ax.legend(ncol=2, loc="lower left", bbox_to_anchor=(0.0, 0.0), frameon=False, handlelength=1.2,
              columnspacing=1.2, borderaxespad=0.3)
    style(ax)

    ax = fig.add_subplot(gs[2, :])
    rows = ["C1", "C2", "C3", "C4", "M"]
    heights = {"C1": 1.0, "C2": 1.0, "C3": 1.0, "C4": 1.0, "M": 1.6}
    ybase, acc = {}, 0.0
    for c in reversed(rows):
        ybase[c] = acc
        acc += heights[c]
    mng = sc["management"]
    for c in rows:
        y, hgt = ybase[c], heights[c]
        for t in range(T):
            fc, txt, hatch, ec, lw = "white", "", None, GRID, 0.6
            if c != "M":
                e = est[c]
                parts = []
                if e["status"][t] == "n/a":
                    fc, parts = FILL_LIGHT, ["n/a"]
                elif e["status"][t] == "n/e":
                    fc, parts = FILL_LIGHT, ["n/e"]
                else:
                    if e["Z"][t]:
                        fc, parts = "#5E5E5E", ["Z"]
                    elif e["J"][t]:
                        hatch, parts = "////", ["J"]
                    if e["E"][t]:
                        parts.append("E")
                        ec, lw = VERMILION, 1.4
                txt = " ".join(parts)
            else:
                notes = []
                dv = mng["M5.2"]["values"][t]
                lo, hi = mng["M5.2"]["target"]
                if isinstance(dv, int) and not lo <= dv <= hi:
                    notes.append(f"{dv:+d}%")
                rl = mng["M5.3"]["values"][t]
                if num(rl) and rl > mng["M5.3"]["target"][1]:
                    notes.append(f"resp. {rl} s")
                tq = mng["M5.4"]["values"][t]
                if num(tq) and tq < mng["M5.4"]["target"][0]:
                    notes.append(f"task {tq}/2")
                txt = "\n".join(notes)
                fc = FILL_LIGHT if notes else "white"
            ax.add_patch(Rectangle((t + 0.55, y + 0.08), 0.9, hgt - 0.16, facecolor=fc, edgecolor=GRID,
                                   linewidth=0.6, hatch=hatch))
            if ec != GRID:
                ax.add_patch(Rectangle((t + 0.55, y + 0.08), 0.9, hgt - 0.16, facecolor="none", edgecolor=ec,
                                       linewidth=lw))
            if txt:
                col = "white" if fc == "#5E5E5E" else INK
                ax.text(t + 1, y + hgt / 2, txt, ha="center", va="center", fontsize=7.0,
                        color=col, fontweight="bold" if c != "M" else "normal", linespacing=1.05)
    ax.set_xlim(0.5, T + 0.5)
    ax.set_ylim(0, acc)
    ax.set_yticks([ybase[c] + heights[c] / 2 for c in rows])
    ax.set_yticklabels(["C1", "C2", "C3", "C4", "M (C5)"])
    ax.set_xticks(ts)
    ax.set_xticklabels(xt)
    ax.tick_params(axis="both", length=0)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_title("(e) Profile flags and management notes", loc="left", fontsize=7.6, color=INK, pad=4)
    save(fig, "fig_4_profile.png")


if __name__ == "__main__":
    main()
