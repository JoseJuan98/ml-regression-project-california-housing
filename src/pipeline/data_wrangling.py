# -*- coding: utf-8 -*-
"""
Date: 02/2023
Version: 1.0
Author: (I) Jose Pena
Website: https://github.com/JoseJuan98

Data Wrangling
==============

Step to wrangle the data, including:
- Cleaning the data
- Format columns
- Drop irrelevant columns or rows
- Format values
...
"""
import numpy
from pandas import DataFrame

from src.pipeline.utils import parse_args, pipe_args


@pipe_args
def wrangle(data: DataFrame) -> DataFrame:
    """
    Clean, select and format data

    Params:
        - data (pandas.DataFrame): The original dataset

    Return:
        - pandas.DataFrame: The processed dataset
    """
    # Columns names formatting
    data.columns = [col.lower().strip() for col in data.columns]

    # Normalize nans
    data = data.replace(["nan", "", " ", None, "NaN"], numpy.nan)

    return data


if __name__ == "__main__":
    # If you want to run it locally in your IDE, create the folder bin, and download the data there
    # Then use the following parameters to run it:
    #   --data-path="../bin" --step-name="Data Wrangling" --output-file="wrangled_data.csv"
    #   --input-file="titanic.csv"
    wrangle(args=parse_args())
