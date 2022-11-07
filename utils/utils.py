# Native libs
import os
from math import ceil
from typing import Union, Literal
from pathlib import Path
from urllib.request import urlretrieve

# Data Analysis
from pandas import DataFrame, read_csv, NA
from matplotlib import pyplot
import seaborn

DOWNLOAD_ROOT = "https://raw.githubusercontent.com/ageron/handson-ml/master/"
HOUSING_PATH = os.path.join('data', 'housing.csv')
HOUSING_URL = os.path.join(DOWNLOAD_ROOT, "datasets/housing/housing.csv")


def fetch_housing_data(url: Union[str, Path],
                       path: Union[str, Path],
                       force_retrieve: bool = False) -> DataFrame:
    """
    Method to extract the data from an URL and stores it in a file into the `path` or if the file already exists in the `path` skips the extraction.
    Finally, returns a dataframe reading this file.
    Args:
        url (str, Path): URL to the source to extract
        path (str, Path): location where to store the csv data
        force_retrieve(bool): if `force_retrive=True` it retrieves data from URL,
                              if `force_retrive=True` it retrieves data only if file doesn't exists

    Returns:
        DataFrame: data extracted from path or URL
    """
    if not os.path.exists(HOUSING_PATH) or force_retrieve:
        dir_path = os.path.dirname(path)

        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)

        urlretrieve(url, path)

    return read_csv(filepath_or_buffer=path, low_memory=False)


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


def remove_outliers_iqr(dataframe: DataFrame, column: str, whisker_width: float = 1.5) -> DataFrame:
    """
    Method to remove outliers from a dataframe by column, including optional whiskers, removing rows
     for which the column value are less than Q1-1.5IQR or greater than Q3+1.5IQR.

    Args:
        dataframe (`:obj:pd.DataFrame`): A pandas dataframe to subset
        column (str): Name of the column to calculate the subset from.
        whisker_width (float): Optional, loosen the IQR filter by a factor of `whisker_width` * IQR.

    Returns:
        (`:obj:pd.DataFrame`): Filtered dataframe
    """
    # Calculate Q1, Q2 and IQR
    q1 = dataframe[column].quantile(0.25)
    q3 = dataframe[column].quantile(0.75)
    iqr = q3 - q1
    # Apply filter with respect to IQR, including optional whiskers
    return dataframe.loc[
        (dataframe[column] >= q1 - whisker_width * iqr) & (dataframe[column] <= q3 + whisker_width * iqr)]


def define_pipeline():
    from sklearn.pipeline import Pipeline
    from sklearn.impute import SimpleImputer

    pipe = Pipeline()

    SimpleImputer(missing_values=NA, strategy='mean')

    return pipe
