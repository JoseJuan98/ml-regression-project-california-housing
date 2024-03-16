# -*- coding: utf-8 -*-
"""Constant variables."""
import pathlib

ROOT_DIR = pathlib.Path(__file__).parent.parent
HOUSING_DATA_URL = "https://raw.githubusercontent.com/ageron/handson-ml2/master/datasets/housing/housing.csv"
target = "median_house_value"
ARTIFACT_DIR = ROOT_DIR / "artifacts"
DATA_DIR = ARTIFACT_DIR / "data"
MODEL_DIR = ARTIFACT_DIR / "models"
RAW_DATA_FILE = DATA_DIR / "california_census.csv"
