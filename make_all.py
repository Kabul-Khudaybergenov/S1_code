"""Draw all figures into ../article/figures as PNG (600 dpi, RGB, white background; MDPI-compliant)."""
import fig_1_conceptual
import fig_2_cycle
import fig_3_mechanism
import fig_4_profile

if __name__ == "__main__":
    for m in (fig_1_conceptual, fig_2_cycle, fig_3_mechanism, fig_4_profile):
        m.main()
