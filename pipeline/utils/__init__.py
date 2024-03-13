# -*- coding: utf-8 -*-
"""Script to include all scripts in this folder in the namespace of utils."""
from pipeline.utils.pipeline import pipe_args, parse_args, create_summary
from pipeline.utils.data_transformations import get_preprocessor, remove_outliers_iqr
from pipeline.utils.data_gathering import fetch_housing_data
from pipeline.utils.visualization import plot_scatters, plot_univariate_boxplots
