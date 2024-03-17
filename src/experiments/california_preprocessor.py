# -*- coding: utf-8 -*-
"""California Census data feature engineering and preprocessing for experiments."""
from typing import Tuple

import numpy
import pandas

from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer, make_column_selector

from exper import Preprocessor, ClusterSimilarityEncoder
from exper.constant import target, HOUSING_DATA_URL, RAW_DATA_FILE
from exper.data_handling import ApiHandler


def columns_ratio(X: numpy.ndarray):
    """Calculates the column ratio between 2 variables.

    This function that follows the scikit-learn API to be used in a ColumnTransformer.
    """
    return X[:, [0]] / X[:, [1]]


def ratio_feature_names_out(function_transformer, feature_names_in):
    """Makes the names of the `features_name_out` in a ColumnTransformer.

    This function that follows the scikit-learn API to be used in a ColumnTransformer.
    """
    return ["ratio"]


def ratio_pipeline() -> Pipeline:
    """Makes the pipeline the calculate the ratio between two variables."""
    return make_pipeline(
        SimpleImputer(strategy="median"),
        FunctionTransformer(func=columns_ratio, feature_names_out=ratio_feature_names_out),
        StandardScaler(with_std=True, with_mean=True),
    )


def log_pipeline() -> Pipeline:
    """Makes the pipeline to smooth a variable."""
    return make_pipeline(
        SimpleImputer(strategy="median"),
        # feature_names_out="one-to-one": features after transformed keep the same name
        FunctionTransformer(func=numpy.log, feature_names_out="one-to-one"),
        StandardScaler(),
    )


def default_numeric_pipeline() -> Pipeline:
    """Makes the pipeline for the numerical variables remaining."""
    return make_pipeline(SimpleImputer(strategy="median"), StandardScaler())


def categorical_pipeline() -> Pipeline:
    """Makes the pipeline for the categorical variables."""
    return make_pipeline(SimpleImputer(strategy="most_frequent"), OneHotEncoder(handle_unknown="ignore"))


class CaliforniaPreprocessor(Preprocessor):
    """California preprocessor.

    Args:
        transformer (sklearn.compose.ColumnTransformer): object with the feature engineering logic
    """

    def __init__(self):
        self.transformer = ColumnTransformer(
            transformers=[
                # combined features
                ("bedrooms", ratio_pipeline(), ["total_bedrooms", "total_rooms"]),
                ("rooms_per_house", ratio_pipeline(), ["total_rooms", "households"]),
                ("people_per_house", ratio_pipeline(), ["population", "households"]),
                # features to be smooth by a log functions
                ("log", log_pipeline(), ["total_bedrooms", "total_rooms", "population", "households", "median_income"]),
                # geospatial features
                (
                    "geospatial",
                    ClusterSimilarityEncoder(n_clusters=10, gamma=1.0, random_state=42),
                    ["latitude", "longitude"],
                ),
                # categorical variables
                ("cat", categorical_pipeline(), make_column_selector(dtype_include=object)),
            ],
            remainder=default_numeric_pipeline(),
        )

    def preprocess(self, data: pandas.DataFrame, transform_data: bool = True) -> pandas.DataFrame:
        """Preprocess the data

        Args:
            data (pandas.DataFrame): Data to be preprocessed
            transform_data (optional, bool): By default False. If true the data will preprocess. Otherwise, it won't.

        Returns:
            pandas.DataFrame: data preprocessed and transformed if transform_data is True
        """
        self.transformer.fit(X=data)

        if transform_data:
            data = self.transformer.transform(X=data)
            data = pandas.DataFrame(data=data, columns=self.transformer.get_feature_names_out())

        return data


if __name__ == "__main__":

    # this is just to test that it works meanwhile developing, that's why it doesn't split between train and test
    housing_data = ApiHandler.load_data(file_path=RAW_DATA_FILE, url=HOUSING_DATA_URL)

    print(f"Raw data:\n{housing_data.head().to_string()}")

    preprocessor = CaliforniaPreprocessor()

    preproc_data = preprocessor.preprocess(data=housing_data, transform_data=True)

    pandas.set_option("display.max_columns", None)
    print(f"\nPreprocessed data:\n{preproc_data.head().to_string()}")
