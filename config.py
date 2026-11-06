"""Shared plotting configuration.

MDPI layout: text width 13.5 cm, full width 17.5 cm.
MDPI figure requirements: raster figures at >= 300 dpi and >= 1000 px on each side,
RGB, opaque white background. We export PNG at 600 dpi (17.5 cm -> ~4134 px wide).
"""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

# Output location. Inside the manuscript project (../article exists) the figures and tables are written
# straight into the LaTeX sources; as a stand-alone repository they go to ./output/.
_ARTICLE = os.path.normpath(os.path.join(HERE, "..", "article"))
if os.path.isdir(_ARTICLE):
    OUT = os.path.join(_ARTICLE, "figures")
    TABLES = os.path.join(_ARTICLE, "tables")
else:
    OUT = os.path.join(HERE, "output", "figures")
    TABLES = os.path.join(HERE, "output", "tables")
os.makedirs(OUT, exist_ok=True)
os.makedirs(TABLES, exist_ok=True)

CM = 1 / 2.54
TEXT_W = 13.5 * CM
FULL_W = 17.5 * CM

# Okabe-Ito categorical order (fixed; never cycled)
BLUE, VERMILION, GREEN, PURPLE = "#0072B2", "#D55E00", "#009E73", "#CC79A7"
ORANGE, SKY, YELLOW = "#E69F00", "#56B4E9", "#F0E442"
INK, INK2, MUTED, GRID = "#1A1A1A", "#4D4D4D", "#8C8C8C", "#D9D9D9"
FILL_LIGHT = "#F2F2F2"
SERIES = {"C1": (BLUE, "o", "-"), "C2": (VERMILION, "s", "--"),
          "C3": (GREEN, "^", "-."), "C4": (PURPLE, "D", ":")}

plt.rcParams.update({
    "font.family": "Arial",
    "font.size": 8,
    "axes.titlesize": 8,
    "axes.labelsize": 8,
    "xtick.labelsize": 7.5,
    "ytick.labelsize": 7.5,
    "legend.fontsize": 7.5,
    "axes.edgecolor": INK2,
    "axes.labelcolor": INK,
    "xtick.color": INK2,
    "ytick.color": INK2,
    "axes.linewidth": 0.6,
    "lines.linewidth": 1.4,
    "savefig.dpi": 600,
    "savefig.format": "png",
    "savefig.facecolor": "white",
    "savefig.edgecolor": "white",
    "savefig.transparent": False,
    "figure.dpi": 150,
})

PNG_DPI = 600          # MDPI: minimum 300 dpi
MIN_PX = 1000          # MDPI: minimum 1000 px width/height


def save(fig, name):
    """Save `fig` as an opaque RGB PNG that meets MDPI figure requirements."""
    if not name.lower().endswith(".png"):
        name = os.path.splitext(name)[0] + ".png"
    path = os.path.join(OUT, name)
    fig.savefig(path, format="png", dpi=PNG_DPI, bbox_inches="tight", pad_inches=0.02,
                facecolor="white", transparent=False,
                pil_kwargs={"dpi": (PNG_DPI, PNG_DPI), "optimize": True})
    plt.close(fig)
    # Flatten to RGB (no alpha channel) and verify size/dpi against MDPI requirements.
    from PIL import Image
    with Image.open(path) as im:
        if im.mode != "RGB":
            bg = Image.new("RGB", im.size, "white")
            bg.paste(im.convert("RGBA"), mask=im.convert("RGBA").split()[-1])
            bg.save(path, format="PNG", dpi=(PNG_DPI, PNG_DPI), optimize=True)
        w, h = im.size
    if min(w, h) < MIN_PX:
        raise SystemExit(f"{name}: {w}x{h} px is below the MDPI minimum of {MIN_PX} px")
    print(f"wrote {path}  ({w}x{h} px, {PNG_DPI} dpi, RGB)")
