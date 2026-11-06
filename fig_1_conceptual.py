"""Figure 1: conceptual model linking educational quality, process quality and lesson delivery quality."""
import matplotlib.pyplot as plt

from config import BLUE, CM, FILL_LIGHT, FULL_W, INK, INK2, save
from diagram import arrow, box, canvas

TINT = "#DCEAF5"


def main():
    fig = plt.figure(figsize=(FULL_W, 9.6 * CM))
    ax = canvas(fig, 100, 55)

    box(ax, 0.5, 0.5, 99, 54, fc="white", ec=INK2, lw=0.9, radius=1.4)
    ax.text(2.0, 52.6, "Educational quality", fontsize=8, fontweight="bold", color=INK, va="top")
    ax.text(2.0, 49.4, "correspondence of goals, content, conditions, processes and outcomes to requirements and needs",
            fontsize=7.2, color=INK2, va="top")

    box(ax, 2.5, 8.5, 73, 37, fc=FILL_LIGHT, ec=INK2, lw=0.8, radius=1.2)
    ax.text(4.0, 43.6, "Quality of the educational process", fontsize=7.6, fontweight="bold", color=INK, va="top")
    ax.text(4.0, 40.6, "content, methods and forms, pedagogical interaction, conditions", fontsize=7.0, color=INK2,
            va="top")

    box(ax, 4.5, 21, 19, 15, "Preconditions\n\nstandards and\ncurricula, resources,\nteacher competence",
        fs=7.2, fc="white")
    box(ax, 32, 21, 23, 15, "Lesson delivery quality\n\nconduct of the lesson:\npedagogical actions,\n"
        "organisation of learning,\nteacher–class interaction", fs=7.2, fc=TINT, ec=BLUE, lw=1.1)
    box(ax, 32, 10.5, 23, 7, "Monitoring and diagnosis\nof lesson characteristics", fs=7.2, fc="white")
    box(ax, 4.5, 10.5, 19, 7, "Diagnostic information\n(profile, flags)", fs=7.2, fc="white")
    box(ax, 80, 21, 18, 15, "Learning\noutcomes\n\nproduced together\nwith individual and\nsocial factors",
        fs=7.2, fc="white")

    arrow(ax, (23.6, 28.5), (31.9, 28.5))
    ax.text(27.75, 29.4, "enacted", fontsize=7.0, color=INK2, ha="center", va="bottom")
    arrow(ax, (43.5, 20.9), (43.5, 17.6))
    ax.text(44.3, 19.2, "observed", fontsize=7.0, color=INK2, ha="left", va="center")
    arrow(ax, (31.9, 14.0), (23.6, 14.0))
    arrow(ax, (14.0, 17.6), (14.0, 20.9), color=BLUE, lw=1.1)
    ax.text(13.2, 19.2, "correction of\nnext lessons", fontsize=7.0, color=BLUE, ha="right", va="center")
    arrow(ax, (23.6, 16.6), (31.9, 22.4), color=BLUE, lw=1.0, rad=-0.25, ls=(0, (3, 2)))
    ax.text(25.2, 20.6, "in-lesson\ncorrection", fontsize=7.0, color=BLUE, ha="left", va="center")
    arrow(ax, (55.1, 28.5), (79.9, 28.5))
    ax.text(67.5, 29.4, "contributes to", fontsize=7.0, color=INK2, ha="center", va="bottom")

    ax.text(2.0, 4.6, "Lesson delivery quality is a process-level factor of learning outcomes and is diagnosed as an "
            "object in its own right, not inferred from achievement.", fontsize=7.0, color=INK2, va="center")
    save(fig, "fig_1_conceptual.png")


if __name__ == "__main__":
    main()
