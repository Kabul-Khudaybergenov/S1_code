"""Figure 2: the diagnostic-regulatory model of lesson delivery quality assurance."""
import matplotlib.pyplot as plt

from config import BLUE, CM, FILL_LIGHT, FULL_W, INK, INK2, VERMILION, save
from diagram import arrow, box, canvas

TINT = "#DCEAF5"
WARM = "#FBE3D4"


def main():
    fig = plt.figure(figsize=(FULL_W, 10.6 * CM))
    ax = canvas(fig, 100, 60.6)

    # inputs and outputs
    box(ax, 0.5, 6, 15.5, 48,
        "Inputs\n\n" "lesson goals,\ncontent and\nstructure\n\n" "class\ncharacteristics\n\n"
        "methods and\nforms of work\n\n" "conditions of the\nlearning\nenvironment",
        fs=7.0, fc=FILL_LIGHT, va="top", ty=52.5)
    box(ax, 84, 6, 15.5, 48,
        "Outcomes\n\n" "structured\ndiagnostic\nprofile Q\n\n" "prompts for\nteacher\nreflection\n\n"
        "professional\ndevelopment\nneeds\n\n" "updated target\nrequirements",
        fs=7.0, fc=FILL_LIGHT, va="top", ty=52.5)

    w, h = 15.0, 8.2
    # top row
    s1 = (19.0, 47.5)
    s2 = (36.5, 47.5)
    box(ax, *s1, w, h, "1  Goal setting and\ncontext-conditioned\ntarget requirements", fs=7.0)
    box(ax, *s2, w, h, "2  Monitoring:\nregistration of\nfeatures X(t)", fs=7.0)
    # right column
    s4 = (65.5, 47.5)
    s5 = (65.5, 26.0)
    box(ax, *s4, w, h, "4  Professional\ninterpretation by\nthe teacher", fs=7.0)
    box(ax, *s5, w, h, "5  Pedagogical\ndecision", fs=7.0)
    # bottom row
    s6 = (65.5, 4.5)
    s7 = (42.0, 4.5)
    s8 = (19.0, 4.5)
    box(ax, *s6, w, h, "6  Correction in the\ncurrent or in\nsubsequent lessons", fs=7.0)
    box(ax, *s7, w + 3, h, "7  Repeated\nmonitoring", fs=7.0)
    box(ax, *s8, w, h, "8  Evaluation of\nchange; update of\nrequirements", fs=7.0)

    # diagnostic module (stage 3)
    mx, my, mw, mh = 22.6, 15.5, 40.0, 27.5
    box(ax, mx, my, mw, mh, fc=TINT, ec=BLUE, lw=1.1, radius=1.4)
    ax.text(mx + 1.2, my + mh - 1.0, "3  Module of pedagogical diagnosis",
            fontsize=7.0, fontweight="bold", color=INK, va="top")
    sub = [("3.1", "Indicator formation", r"$\mathcal{F}_1: X \to P$;  $X \to M$"),
           ("3.2", "Latent-characteristic estimation", r"$\mathcal{F}_2: (P, \mathcal{C}) \to (\hat{L}, u)$"),
           ("3.3", "Dynamics and interrelations", r"$\mathcal{F}_3: (P, \hat{L}) \to D$"),
           ("3.4", "Profile integration", r"$\mathcal{F}_4: (P, \hat{L}, u, D, M, \mathcal{C}) \to Q$"),
           ("3.5", "Flagging", "problem zones Z, referrals J, events E")]
    yy = my + mh - 4.4
    for code, name, formula in sub:
        box(ax, mx + 1.2, yy - 3.9, mw - 2.4, 4.0, fc="white", ec=BLUE, lw=0.6, radius=0.8)
        ax.text(mx + 2.2, yy - 1.9, f"{code}  {name}", fontsize=7.0, color=INK, va="center")
        ax.text(mx + mw - 2.2, yy - 1.9, formula, fontsize=7.0, color=INK2, va="center", ha="right")
        yy -= 4.55

    # cycle arrows
    arrow(ax, (s1[0] + w + 0.1, s1[1] + h / 2), (s2[0] - 0.1, s2[1] + h / 2))
    arrow(ax, (s2[0] + w / 2, s2[1] - 0.1), (s2[0] + w / 2, my + mh + 0.1))
    arrow(ax, (mx + mw + 0.1, my + mh - 3.0), (s4[0] - 0.1, s4[1] + h / 2), rad=-0.25)
    arrow(ax, (s4[0] + w / 2, s4[1] - 0.1), (s5[0] + w / 2, s5[1] + h + 0.1))
    arrow(ax, (s5[0] + w / 2, s5[1] - 0.1), (s6[0] + w / 2, s6[1] + h + 0.1))
    arrow(ax, (s6[0] - 0.1, s6[1] + h / 2), (s7[0] + w + 3 + 0.1, s7[1] + h / 2))
    arrow(ax, (s7[0] - 0.1, s7[1] + h / 2), (s8[0] + w + 0.1, s8[1] + h / 2))
    arrow(ax, (s8[0] + 1.5, s8[1] + h + 0.1), (s1[0] + 1.5, s1[1] - 0.1), color=VERMILION, lw=1.1)
    ax.text(s8[0] + 0.7, 30.0, "closed cycle", fontsize=7.0, color=VERMILION, va="center", ha="right",
            rotation=90)

    # inputs / outputs connections
    arrow(ax, (16.1, 51.6), (18.9, 51.6))
    arrow(ax, (80.6, 30.1), (83.9, 30.1))
    arrow(ax, (80.6, 51.6), (83.9, 51.6))

    ax.text(42.0, 58.9, "AI-based technologies may support stages 2–3 (registration, indicator formation, analytics); "
            "stages 4–6 remain with the teacher.", fontsize=7.0, color=INK2, ha="center", va="center")
    save(fig, "fig_2_cycle.png")


if __name__ == "__main__":
    main()
