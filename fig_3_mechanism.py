"""Figure 3: multi-level mechanism of comprehensive pedagogical diagnosis, Q = F(P, L-hat, u, D, M, C)."""
import matplotlib.pyplot as plt

from config import BLUE, CM, FILL_LIGHT, FULL_W, GREEN, INK, INK2, VERMILION, save
from diagram import arrow, box, canvas

TINT = "#DCEAF5"
GREEN_T = "#D9F0E8"
WARM = "#FBE3D4"


def main():
    fig = plt.figure(figsize=(FULL_W, 8.25 * CM))
    ax = canvas(fig, 100, 53.7)

    # context band
    box(ax, 39.5, 46.0, 59.5, 6.6, fc=WARM, ec=VERMILION, lw=0.8, radius=1.0)
    ax.text(69.25, 49.3, "Context $\\mathcal{C}$: lesson stage, activity form, class characteristics\n"
            r"$\rightarrow$ context-conditioned target ranges $[a_k(c), b_k(c)]$", fontsize=7.0, color=INK,
            va="center", ha="center")

    # main chain
    y, h = 26.5, 14.0
    xs = {"X": 1.0, "P": 20.5, "L": 40.0, "D": 59.5, "Q": 80.0}
    w = 15.5
    box(ax, xs["X"], y, w, h, "Observable\nfeatures $X(t)$\n\nevents, actions,\nutterances", fs=7.0, fc="white")
    box(ax, xs["P"], y, w, h, "Indicators $P(t)$\n\nfrequency, duration,\nshare, intensity,\nstability", fs=7.0,
        fc=TINT, ec=BLUE)
    box(ax, xs["L"], y, w, h, "Latent estimates\n$\\hat{L}_j(t) \\pm u_j(t)$\n\nC1–C4; uncertainty\nretained", fs=7.0,
        fc=TINT, ec=BLUE)
    box(ax, xs["D"], y, w, h, "Dynamics and\ninterrelations $D$\n\nlevels, variability,\njumps,\nco-variation",
        fs=7.0, fc=TINT, ec=BLUE)
    box(ax, xs["Q"], y, w + 3.5, h, "Diagnostic profile $Q$\n\nstructured, not a\nsingle score; flags\n"
        "Z, J and E", fs=7.0, fc=GREEN_T, ec=GREEN, lw=1.0)

    ops = [("X", "P", r"$\mathcal{F}_1$"), ("P", "L", r"$\mathcal{F}_2$"), ("L", "D", r"$\mathcal{F}_3$"),
           ("D", "Q", r"$\mathcal{F}_4$")]
    for a, b, lab in ops:
        arrow(ax, (xs[a] + w + 0.1, y + h / 2), (xs[b] - 0.1, y + h / 2), lw=1.0)
        ax.text((xs[a] + w + xs[b]) / 2, y + h / 2 + 1.0, lab, fontsize=7.5, color=INK, ha="center",
                va="bottom")

    # non-strict sequencing (dashed arcs below the chain)
    arrow(ax, (xs["P"] + w * 0.7, y - 0.1), (xs["D"] + w * 0.3, y - 0.1), rad=0.32, ls=(0, (3, 2)), lw=0.8)
    arrow(ax, (xs["L"] + w * 0.7, y - 0.1), (xs["Q"] + w * 0.4, y - 0.1), rad=0.32, ls=(0, (3, 2)), lw=0.8)
    ax.text(49.5, 18.4, "non-strict sequencing: $\\mathcal{F}_3$ uses $P$ and $\\hat{L}$; $\\mathcal{F}_4$ uses "
            "$P$, $\\hat{L}$, $u$, $D$, $M$, $\\mathcal{C}$", fontsize=7.0, color=INK2, ha="center", va="center")

    # context arrows
    arrow(ax, (xs["L"] + w / 2, 45.9), (xs["L"] + w / 2, y + h + 0.1), color=VERMILION, lw=0.9)
    arrow(ax, (xs["Q"] + w / 2 + 1.5, 45.9), (xs["Q"] + w / 2 + 1.5, y + h + 0.1), color=VERMILION, lw=0.9)

    # management branch
    box(ax, 1.0, 8.0, 34.0, 9.5, "Management indicators $M(t)$ (C5)\ngoal clarity, timing, responsiveness, "
        "task setting\n(largely observable; attributable to the teacher)", fs=7.0, fc=FILL_LIGHT)
    arrow(ax, (xs["X"] + 5.0, y - 0.1), (xs["X"] + 5.0, 17.6), lw=0.9)
    ax.text(xs["X"] + 5.8, 21.6, r"$\mathcal{F}_1^{M}$", fontsize=7.2, color=INK, ha="left", va="center")
    ax.plot([35.1, xs["Q"] + 1.5], [12.75, 12.75], color=INK2, linewidth=0.9, zorder=5)
    arrow(ax, (xs["Q"] + 1.5, 12.7), (xs["Q"] + 1.5, y - 0.1), lw=0.9)

    # teacher in the loop
    box(ax, 83.5, 9.0, 15.5, 8.0, "Teacher interprets\nand decides", fs=7.0, fc="white", ec=GREEN, lw=1.0)
    arrow(ax, (xs["Q"] + 12.5, y - 0.1), (xs["Q"] + 12.5, 17.1), color=GREEN, lw=1.0)

    ax.set_ylim(6.8, 53.7)
    save(fig, "fig_3_mechanism.png")


if __name__ == "__main__":
    main()
