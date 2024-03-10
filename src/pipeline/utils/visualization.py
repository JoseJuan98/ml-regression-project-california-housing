# -*- coding: utf-8 -*-
"""
Date: 02/2023
Version: 1.0
Author: (I) Jose Pena
Website: https://github.com/JoseJuan98


Title
=====

...
"""
from math import ceil
from typing import Literal

import seaborn
from matplotlib import pyplot
from pandas import DataFrame


def __create_grid_for_plots(data: DataFrame, variables: list, ncols: int, plot: Literal['boxplot', 'scatter'],
                            target: str = None) -> None:
    nrows = ceil(len(variables) / ncols)

    figsize = (20 * ncols, 15 * nrows)
    if plot == 'boxplot':
        figsize = (45, 55)
        seaborn.set(rc={"figure.figsize": (40, 50)})

    fig, axes = pyplot.subplots(nrows=nrows, ncols=ncols, figsize=figsize)

    idx = 0
    for i in range(nrows):
        if idx >= len(variables):
            axes[i, 0].set_visible(False)
            break
        for j in range(ncols):
            # if plot == 'boxplot':
            if idx >= len(variables):
                for new_j in range(j, ncols):
                    axes[i, new_j].set_visible(False)
                break
            att = variables[idx]
            idx += 1
            # else:
            #     att = variables[i + j]

            if plot == 'boxplot':
                fontsize = 30
                labelsize = 26
            else:
                fontsize = 25
                labelsize = 16

            axes[i, j].set_xlabel(f'{att}', fontsize=fontsize)
            axes[i, j].tick_params(axis='both', which='major', labelsize=labelsize)
            axes[i, j].tick_params(axis='both', which='minor', labelsize=labelsize)

            if plot == 'boxplot':
                seaborn.boxplot(x=data[att], ax=axes[i, j])

            elif plot == 'scatter':
                axes[i, j].scatter(x=data[att], y=data[target], alpha=0.5);
                axes[i, j].set_ylabel(f'{target}', fontsize=fontsize)
            else:
                raise AttributeError(f'Invalid value {plot} for argument plot')

    pyplot.show();


def plot_scatters(data, variables: list, target: str, ncols: int = 2) -> None:
    """
    Method to plot the scatter plot of the specified variables and the target variable

    Args:
        data: dataframe with the data
        variables: columns scpecified to plot. By default, all
        ncols: number of plots per row.
        target: target variable name

    Returns:

    """
    __create_grid_for_plots(data=data, variables=variables, ncols=ncols, target=target, plot='scatter')


def plot_univariate_boxplots(data: DataFrame, variables: list = None, ncols: int = 2) -> None:
    """
    Method to plot bloxplots of the specified variables, or all by default, of the dataframe, useful for
    uni-variate analisis of outliers.

    Args:
        data: dataframe with the data
        variables: columns scpecified to plot. By default, all
        ncols: number of plots per row.

    Returns:

    """
    if variables is None:
        variables = data.select_dtypes('number').columns.to_list()

    __create_grid_for_plots(data=data, ncols=ncols, variables=variables, plot='boxplot')

    seaborn.set(rc={"figure.figsize": (12, 7)})
