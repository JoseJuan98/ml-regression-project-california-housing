import os
from pathlib import Path

DOWNLOAD_ROOT = "https://raw.githubusercontent.com/ageron/handson-ml/master/"
DATA_PATH = os.path.join(Path(__file__).parent.parent.parent, 'data')
HOUSING_PATH = os.path.join(DATA_PATH, 'housing.csv')
PREPARED_DATA = os.path.join(DATA_PATH, 'housing_prepared.csv')
HOUSING_URL = os.path.join(DOWNLOAD_ROOT, "datasets/housing/housing.csv")
