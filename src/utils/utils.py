# Native libs
import os
import logging
from typing import Union
from pathlib import Path
from urllib.request import urlretrieve

# Data Analysis
from pandas import DataFrame, read_csv

# Machine Learning procedures

# Utils
# from src.utils import
logger = logging.getLogger('main')
logger.addHandler(logging.StreamHandler())

DOWNLOAD_ROOT = "https://raw.githubusercontent.com/ageron/handson-ml/master/"
DATA_PATH = os.path.join(Path(__file__).parent.parent.parent, 'data')
HOUSING_PATH = os.path.join(DATA_PATH, 'housing.csv')
PREPARED_DATA = os.path.join(DATA_PATH, 'housing_prepared.csv')
HOUSING_URL = os.path.join(DOWNLOAD_ROOT, "datasets/housing/housing.csv")
TARGET = 'median_house_value'


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


