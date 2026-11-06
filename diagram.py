"""Small helpers for vector box-and-arrow diagrams (Figures 1-3)."""
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

from config import INK, INK2


def box(ax, x, y, w, h, text="", fc="white", ec=INK2, lw=0.8, fs=7.5, weight="normal", ha="center",
        va="center", pad=0.6, radius=1.2, color=INK, ls="-", z=2, tx=None, ty=None, linespacing=1.15):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={radius}", facecolor=fc,
                       edgecolor=ec, linewidth=lw, linestyle=ls, zorder=z)
    ax.add_patch(p)
    if text:
        if tx is None:
            tx = x + w / 2 if ha == "center" else (x + pad if ha == "left" else x + w - pad)
        if ty is None:
            ty = y + h / 2 if va == "center" else (y + h - pad if va == "top" else y + pad)
        ax.text(tx, ty, text, ha=ha, va=va, fontsize=fs, fontweight=weight, color=color, zorder=z + 1,
                linespacing=linespacing)
    return p


def arrow(ax, p1, p2, color=INK2, lw=0.9, style="-|>", rad=0.0, ls="-", z=5, ms=7, shrinkA=1, shrinkB=1):
    a = FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=ms, color=color, linewidth=lw,
                        connectionstyle=f"arc3,rad={rad}", linestyle=ls, zorder=z, shrinkA=shrinkA,
                        shrinkB=shrinkB)
    ax.add_patch(a)
    return a


def canvas(fig, xmax=100, ymax=60):
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, xmax)
    ax.set_ylim(0, ymax)
    ax.axis("off")
    return ax
