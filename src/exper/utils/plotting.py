# -*- coding: utf-8 -*-
"""Plot utils."""
import matplotlib
import seaborn


def set_plotting_style() -> None:
    """Set matplotlib and seaborn style."""
    plot_config = {
        "legend.fontsize": "x-large",
        "figure.figsize": (18, 13),
        "axes.labelsize": 22,
        "axes.titlesize": 24,
        "xtick.labelsize": 22,
        "ytick.labelsize": 22,
        "figure.dpi": 200,
    }

    matplotlib.rcParams.update(plot_config)
    seaborn.set_style(rc=matplotlib.rcParams)
