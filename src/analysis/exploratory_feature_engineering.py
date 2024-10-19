# -*- coding: utf-8 -*-
"""California Census Feature Engineering Exploration."""
import os

import numpy
import pandas
import seaborn
from matplotlib import pyplot

from exper.constant import RAW_DATA_FILE, HOUSING_DATA_URL, PLOT_DIR
from exper.data_handling import ApiHandler
from exper.utils import set_plotting_style


def exploratory_feature_engineering(data: pandas.DataFrame) -> None:
    """Exploratory Feature Engineering."""

    set_plotting_style()

    print("=> Data Cleaning\n")
    print(f"Checking variables with missing values:\n{data.isnull().sum()}\n")
    print(
        "Total number of bedrooms has 207 missing values. This can be handle by imputing by the median value of this"
        " variable."
    )

    total_bedrooms_median = data["total_bedrooms"].median()
    data.fillna(value={"total_bedrooms": total_bedrooms_median}, inplace=True)
    print(f"\nMissing values after imputation:\n{data.isnull().sum()}")

    print("\n\n=> Feature Engineering\n")

    print(
        "Another aspect to take care of is as it was shown in the exploratory data analysis, some of the variables"
        " are very skewed. To handle this a method to smooth the distribution can be used, such as using the log"
        " function, the square root or more complex ones like the power law. As, in many ML techniques, the more"
        " complex the less interpretable, so for that reason I decided to use the log function."
    )

    print(
        "As this dataset is based in the median value of the variables per district, it can be interesting to"
        " explore the combination of some of the variables with the number of households, such as total rooms per"
        " household and population per household. The number of households per district is hold"
        " in the variable 'households'.\n"
    )

    skewness = data.select_dtypes(include="number").skew().sort_values(ascending=False)
    print(f"Skewness of variables:\n{skewness}\n")

    # -0.5 < skweness > 0.5 is moderately skewed, and -1 < skweness > 1 is severely skewed.
    skewed_cols = skewness[(skewness > 0.5) | (skewness < -0.5)].index.tolist()
    print(f"Moderately and severely skewed variables:\n{skewed_cols}\n")

    # fixing skweness with the log function
    for col in skewed_cols:
        data[col] = numpy.log(data[[col]])

    print(f"Skewness after applying the log:\n{data[skewed_cols].skew().sort_values(ascending=False)}\n")

    data["rooms_per_household"] = data["total_rooms"] / data["households"]
    data["people_per_household"] = data["population"] / data["households"]

    print("Another combined variable can be the ratio of bedrooms per total number of rooms.")
    data["bedrooms_ratio"] = data["total_bedrooms"] / data["total_rooms"]

    corr_matrix = data.select_dtypes(include="number").corr()["median_house_value"].sort_values(ascending=False)
    print(
        "By seeing the correlation with this new variables, it's possible to check if this combinations are useful. "
        f"\n\nNew correlations:\n{corr_matrix[1:,]}\n"
    )

    print(
        "For ease of experimenting and reproducibility with the models,all this logic has been encapsulated into the "
        "'experiment.preprocessor.CaliforniaPreprocessor' class."
    )


if __name__ == "__main__":
    data = ApiHandler.load_data(file_path=RAW_DATA_FILE, url=HOUSING_DATA_URL)

    exploratory_feature_engineering(data=data)
