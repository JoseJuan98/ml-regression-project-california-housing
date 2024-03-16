# -*- coding: utf-8 -*-
"""California Census data profiling."""
import os

import pandas
from matplotlib import pyplot, rcParams

from exper.contant import RAW_DATA_FILE, HOUSING_DATA_URL, PLOT_DIR
from exper.data_handling import ApiHandler


def data_summary(data: pandas.DataFrame) -> None:

    print(f"Dataset:\n\n{data.head().to_string()}\n")
    print(f"Shape of dataset {data.shape}\n")
    print(f"Variables: {data.columns.tolist()}\n")
    print(f"Data description:\n\n{data.describe(include='all').to_string()} \n")

    print("Geospatial plot:\n")
    rcParams["figure.dpi"] = 200
    data.plot(
        kind="scatter",
        x="longitude",
        y="latitude",
        alpha=0.9,
        s=data["population"] / 100,
        label="population",
        figsize=(18, 13),
        c="median_house_value",
        cmap=pyplot.get_cmap("jet"),
        colorbar=True,
    )
    pyplot.title("Population Density and Housing Price", fontsize=24)
    pyplot.xlabel("Longitude", fontsize=22)
    pyplot.ylabel("Latitude", fontsize=22)
    os.makedirs(PLOT_DIR, exist_ok=True)
    pyplot.savefig(PLOT_DIR / "population_density_and_price.png")
    pyplot.show()


if __name__ == "__main__":
    data = ApiHandler.load_data(file_path=RAW_DATA_FILE, url=HOUSING_DATA_URL)

    data_summary(data=data)
