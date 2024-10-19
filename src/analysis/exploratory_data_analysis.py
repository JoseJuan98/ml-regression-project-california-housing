# -*- coding: utf-8 -*-
"""California Census data profiling."""
import os

import pandas
import seaborn
from matplotlib import pyplot
from pandas.plotting import scatter_matrix

from exper.constant import RAW_DATA_FILE, HOUSING_DATA_URL, PLOT_DIR
from exper.data_handling import ApiHandler
from exper.utils import set_plotting_style


def exploratory_data_analysis(data: pandas.DataFrame) -> None:

    print("This section's purpose is mainly to gather insights through statistics and visualization.\n")
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

    corr_matrix = data.select_dtypes(include="number").corr()["median_house_value"].sort_values(ascending=False)
    # the [1:,] is to remove the correlation of median house value with itself
    print(f"Correlations:\n{corr_matrix[1:,].to_string()}\n")

    print("Correlation horizontal bar plot:")
    corr_matrix[1:,].sort_values(ascending=True).plot(kind="barh", figsize=(18, 13))
    pyplot.title("Correlation Bar Plot")
    pyplot.axvline(x=0, color=".5")
    pyplot.subplots_adjust(left=0.5)
    pyplot.savefig(PLOT_DIR / "correlation_hbar_plot.png")
    pyplot.show()

    # variables when -0.05 > p-value > 0.05 (as correlation belongs [-1,1]), including the target variable
    highly_correlated_variables = corr_matrix[(0.05 < corr_matrix) | (corr_matrix < -0.05)].index.tolist()
    print(f"\nMost correlated variables:\n{highly_correlated_variables}\n")

    print("\nScatter matrix of most correlated variables:\n")
    print(
        "Latitude is excluded from the visualization as it's not a continous variable, it will be difficult"
        "to interpret its scatter plot with the target variable and later its box-plot.\n"
    )
    highly_correlated_variables.remove("latitude")
    scatter_matrix(data[highly_correlated_variables], figsize=(30, 25))
    pyplot.savefig(PLOT_DIR / "scatter_matrix.png")
    pyplot.show()

    print("Scatter matrix of median_income:\n")

    data.plot(kind="scatter", x="median_income", y="median_house_value", alpha=0.3, grid=True, figsize=(18, 13))
    pyplot.title("Median Income vs Median House Value")
    pyplot.savefig(PLOT_DIR / "income_vs_house_value.png")
    pyplot.show()

    print("Boxplots of most correlated variables:\n")

    for col in highly_correlated_variables:
        seaborn.boxplot(x=data[col])
        pyplot.savefig(PLOT_DIR / f"boxplot_{col}.png")
        pyplot.show()


if __name__ == "__main__":
    housing_data = ApiHandler.load_data(file_path=RAW_DATA_FILE, url=HOUSING_DATA_URL)

    exploratory_data_analysis(data=housing_data)
