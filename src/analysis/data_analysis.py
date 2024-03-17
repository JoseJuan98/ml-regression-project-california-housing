# -*- coding: utf-8 -*-
"""California Census data profiling."""
import os

import matplotlib
import pandas
import seaborn
from matplotlib import pyplot
from pandas.plotting import scatter_matrix

from exper.constant import RAW_DATA_FILE, HOUSING_DATA_URL, PLOT_DIR
from exper.data_handling import ApiHandler
from exper.utils import set_plotting_style


def data_analysis(data: pandas.DataFrame) -> None:

    print(f"Dataset:\n\n{data.head().to_string()}\n")
    print(f"Shape of dataset {data.shape}\n")
    print(f"Variables: {data.columns.tolist()}\n")
    print(f"Data description:\n\n{data.describe(include='all').to_string()} \n")

    print("Geospatial plot of the population density and housing prices in California:\n")

    # set plot styles for matplotlib and seaborn for cleaner visualizations
    set_plotting_style()

    # make the directory if it doesn't exist
    os.makedirs(PLOT_DIR, exist_ok=True)

    data.plot(
        kind="scatter",
        x="longitude",
        y="latitude",
        alpha=0.9,
        s=data["population"] / 100,
        label="population",
        figsize=(18, 13),
        c="median_house_value",
        cmap="jet",
        colorbar=True,
        grid=True,
    )

    pyplot.title("California Population Density and Housing Price")
    pyplot.xlabel("Longitude")
    pyplot.ylabel("Latitude")
    pyplot.savefig(PLOT_DIR / "population_density_and_price.png")
    pyplot.show()

    print("Distribution plot/Histogram of the Median House Value:\n")

    plot = seaborn.displot(data["median_house_value"], height=10, aspect=2, kde=True)
    plot.fig.suptitle("Median House Value", fontsize=24)
    pyplot.ylabel("Number of districts")
    pyplot.savefig(PLOT_DIR / "median_house_value_distribution.png")
    pyplot.show()

    print(f"Skewness of Median House Value: {data.median_house_value.skew():.4f}\n")

    print("Histograms of numerical variables:\n")
    data.hist(bins=50, figsize=(30, 25))
    pyplot.ylabel("Number of districts")
    pyplot.suptitle("Histograms of variables", fontsize=26)
    pyplot.savefig(PLOT_DIR / "variables_histogram.png")
    pyplot.show()

    print("Bar plot of the Ocean Proximity variable :\n")
    data.ocean_proximity.value_counts().sort_values(ascending=False).plot(kind="bar", figsize=(18, 13))
    pyplot.title("Ocean Proximity")
    pyplot.savefig(PLOT_DIR / "ocean_proximity.png")
    pyplot.show()

    print("Correlation matrix\n")
    corr_matrix = data.select_dtypes(include="number").corr()["median_house_value"].sort_values(ascending=False)
    corr_matrix.plot(kind="barh", figsize=(18, 13))
    pyplot.title("Correlation Bar Plot")
    pyplot.axvline(x=0, color=".5")
    pyplot.subplots_adjust(left=0.5)
    pyplot.show()

    # FIXME: internal server error
    # print("Scatter matrix of numerical variables:\n")
    #
    # # lower resolution as it's expensive computationally
    # matplotlib.RcParams.update(
    #     {
    #         "figure.dpi": 75,
    #     }
    # )
    #
    # scatter_matrix(data.select_dtypes(include="number"), figsize=(30, 25))
    # pyplot.savefig(PLOT_DIR / "scatter_matrix.png")
    # pyplot.show()
    #
    # matplotlib.RcParams.update(
    #     {
    #         "figure.dpi": 200,
    #     }
    # )


if __name__ == "__main__":
    housing_data = ApiHandler.load_data(file_path=RAW_DATA_FILE, url=HOUSING_DATA_URL)

    data_analysis(data=housing_data)
