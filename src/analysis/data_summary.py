# -*- coding: utf-8 -*-
"""California Census data profiling."""
import pandas

from exper.contant import RAW_DATA_FILE, HOUSING_DATA_URL
from exper.data_handling import ApiHandler


def data_summary(data: pandas.DataFrame) -> None:

    print(f"Shape of dataset {data.shape}\n")
    print(f"Variables: {data.columns.tolist()}\n")
    print(f"Data: {data.head()}\n")


if __name__ == "__main__":
    data = ApiHandler.load_data(file_path=RAW_DATA_FILE, url=HOUSING_DATA_URL)

    data_summary(data=data)
