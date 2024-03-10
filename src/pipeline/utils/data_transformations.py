# -*- coding: utf-8 -*-
"""
Date: 02/2023
Version: 1.0
Author: (I) Jose Pena
Website: https://github.com/JoseJuan98


Data Transformations
====================

...
"""
import re
import logging

from typing import Union, Any

import numpy
from pandas import DataFrame, NA, concat, Series
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler
from sklearn.utils import resample

from scipy.stats import boxcox

from src.pipeline.config.constants import TARGET
from src.pipeline.utils import logger


def remove_outliers_iqr(dataframe: DataFrame, columns: list[str] | str, whisker_width: float = 1.5) -> DataFrame:
    """
    Method to remove outliers from a dataframe by column, including optional whiskers, removing rows
     for which the column value are less than Q1-1.5IQR or greater than Q3+1.5IQR.

    Args:
        dataframe (`:obj:pandas.DataFrame`): A pandas dataframe to subset
        columns (list[str] | str): Name of the column to calculate the subset from.
        whisker_width (float): Optional, loosen the IQR filter by a factor of `whisker_width` * IQR.

    Returns:
        (`:obj:pd.DataFrame`): Filtered dataframe
    """
    if isinstance(columns, str):
        columns = [columns]

    for col in columns:
        # Calculate Q1, Q2 and IQR
        q1 = dataframe[col].quantile(0.25)
        q3 = dataframe[col].quantile(0.75)
        iqr = q3 - q1

        # Apply filter with respect to IQR, including optional whiskers
        dataframe[col] = dataframe[col].loc[(dataframe[col] >= q1 - whisker_width * iqr) &
                                            (dataframe[col] <= q3 + whisker_width * iqr)]

    return dataframe


def normalize_column(data: DataFrame | Series | numpy.ndarray,
                     lmbda: int | None = None) -> Union[DataFrame, Any]:
    """

    Args:
        lmbda (int):
        data (pandas.DataFrame):

    Returns:

    """

    if isinstance(data, DataFrame):
        if data.shape[1] <= 0:
            data = data.to_numpy()
        else:
            raise Exception(f"DataFrame with dimesions {data.shape} must be of 1-dimesion")

    # Normalizing target variable
    if lmbda:
        data = DataFrame(data=(boxcox(data,
                                      lmbda=lmbda)
                               .reshape(-1, 1)
                               )
                         )
    else:
        bc_result = boxcox(data)
        data = DataFrame(data=bc_result[0].reshape(-1, 1))
        lmbda = bc_result[1]

    return data, lmbda


def get_preprocessor(categorical_columns: list[str],
                     numerical_columns: list[str]) -> ColumnTransformer:
    """
    Returns:
        ColumnTransformer: pipeline with the data preparation for a ml model
    """
    _categorical_pipeline = Pipeline(steps=[
        ('cat_imputer', SimpleImputer(missing_values=numpy.nan, strategy='most_frequent')),
        ('cat_ohe', OneHotEncoder(handle_unknown='ignore', sparse_output=True))
    ], verbose=True)

    _numerical_pipeline = Pipeline(steps=[
        ('num_imputer', SimpleImputer(missing_values=NA, strategy='mean')),
        ('scaler', MinMaxScaler(feature_range=(0, 1)))
    ], verbose=True)

    # Generate pipeline
    return ColumnTransformer(transformers=[
        ('numerical', _numerical_pipeline, numerical_columns),
        ('categorical', _categorical_pipeline, categorical_columns)
    ], verbose=True, n_jobs=-1, remainder='passthrough')


def preprocess_data(X: DataFrame,
                    y: DataFrame | Series | numpy.ndarray,
                    normalize_target: bool = False,
                    normalization_lmbda: int | None = None,
                    variables_with_outliers: Union[list[str], str, None] = None,
                    preprocessor: Union[Any, None] = None,
                    verbose: bool = False) -> Union[DataFrame, Any, Any, Any]:
    """Module to preprocess the data for Machine Learning models and create the artifacts
    needed to preprocess of the test set.

    Description:
        It contains:
            - (Optional) The normalization of the target variable
            - (Optional) Removing outliers
            - The Feature Engineering of the features (scaling, encoding, interpolation ...)

    Args:
        X
        y
        normalization_lmbda:
        normalize_target
        variables_with_outliers
        preprocessor: By default None. Already fit Column Transformer Pipeline passed to perform
                      the feature engineering.
        verbose

    Returns:
        Tuple[DataFrame, Any, Pipeline, Any]: it returns in order:
            - The transformed dependent variables (X, x_train)
            - The transformed independent variable (y, y_train)
            - The `:ob:sklearn.pipeline.Pipeline` object with the fit logic to transform the features
            - The lambda function used by the boxcox module to perform the normalization of the target,
                it can be use later to inverse the transformation and get the correct target value.

    """
    if verbose:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.ERROR)

    logger.info(f"{'':_^30} Preparing Data {'':_^30}")

    msg = f"\n\t-> Handling missing values. \n" + \
          f"\t\tMissing values of `total_bedrooms`:\n" + \
          f"{'':>30}{'Before':10}: {X.total_bedrooms.isna().sum()}"

    lamb = None
    if normalize_target:
        # msg += f"{'':>30}{'Old':10}: {y.skew():.4f}. \n"
        y, lamb = normalize_column(data=y, lmbda=normalization_lmbda)
        # msg += f"{'':>30}{'Current':10}: {y.skew():.4f}\n"

    # Handling outliers
    if variables_with_outliers is not None:
        msg += f"{'':>30}{'After':10}: {X.total_bedrooms.isna().sum()}" + \
               f"\n\n\t-> Handling outliers."
        X = remove_outliers_iqr(dataframe=X, columns=variables_with_outliers, whisker_width=1.5)

    cat_cols = X.select_dtypes(include=["O", "object", "string"]).columns.to_list()
    num_cols = X.select_dtypes(include=["number"]).columns.to_list()

    if preprocessor is None:
        preprocessor = get_preprocessor(
            categorical_columns=cat_cols,
            numerical_columns=num_cols
        )

        preprocessor.fit(X=X, y=y)

    X = preprocessor.transform(X=X)

    columns = [re.sub('categorical__|numerical__', '', col) for
               col in preprocessor.get_feature_names_out()]

    X = DataFrame(X, columns=columns)

    logger.info(msg)

    return (X,
            y,
            preprocessor,
            lamb)


def prepare_data(data: DataFrame, target: str, verbose: bool = False) -> DataFrame:
    """

    Args:
        verbose (bool): if True it will print the messages, if not it won't
        target (str): name of the target variable
        data (pandas.DataFrame): raw data to be prepared

    Returns:
        pandas.DataFrame: prepared data
    """
    logger.warning(DeprecationWarning('This module in the future will be deprecated' +
                                      'by `preprocess_data()`'))
    if verbose:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.ERROR)

    logger.info(f"{'':_^30} Preparing Data {'':_^30}")

    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import OneHotEncoder, MinMaxScaler

    # Normalizing target variable
    old_skewness = data[target].skew()
    data, lamb = normalize_column(data=data, column=target)

    logger.info(f"\t-> Target normalization. \n\t\tSkewness: \n"
                f"{'':>30}{'Old':10}: {old_skewness:.4f}. \n"
                f"{'':>30}{'Current':10}: {data[target].skew():.4f}\n"
                f"\n\t-> Handling missing values. \n"
                f"\t\tMissing values of `total_bedrooms`:\n"
                f"{'':>30}{'Before':10}: {data.total_bedrooms.isna().sum()}")

    # Missing values
    imputer = SimpleImputer(missing_values=numpy.nan, strategy='mean')
    data.total_bedrooms = imputer.fit_transform(X=data.total_bedrooms.to_numpy().reshape(-1, 1))

    logger.info(f"{'':>30}{'After':10}: {data.total_bedrooms.isna().sum()}"
                f"\n\n\t-> Handling outliers.")

    # Handling outliers
    variables_with_outliers = ["median_income", "total_rooms", "total_bedrooms", "population", "median_income",
                               "housing_median_age", "households"]

    data = remove_outliers_iqr(dataframe=data, columns=variables_with_outliers, whisker_width=1.5)

    # Encoding categorical variables
    logger.info(f"\t-> Encoding categorical variables.")
    categorical_variables = data.select_dtypes('object').columns.to_list()
    cat_encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    original_index = data[categorical_variables].index

    new_cat_data = cat_encoder.fit_transform(data[categorical_variables])
    new_cat_columns = cat_encoder.get_feature_names_out().tolist()

    new_cat_data = DataFrame(data=new_cat_data, columns=new_cat_columns)
    new_cat_data.set_index(original_index, inplace=True)
    data = concat([data, new_cat_data], axis=1, join='inner')
    del new_cat_data, original_index
    data.drop(columns=categorical_variables, inplace=True, axis=1)

    # Scaling numerical variables
    logger.info(f"\t-> Scaling continuous variables.\n")
    norm_cols = [col for col in data.columns.tolist() if col not in new_cat_columns + [TARGET]]

    norm_data = MinMaxScaler().fit_transform(data[norm_cols])
    original_index = data[norm_cols].index

    norm_data = DataFrame(data=norm_data, columns=norm_cols)
    norm_data.set_index(original_index, inplace=True)
    data[norm_cols] = norm_data[norm_cols]
    del norm_data, original_index

    return data, lamb


def resample_by_category(target: str,
                         x_train: DataFrame,
                         up_or_down: str = 'up',
                         resampling_perc: float = 1.0) -> DataFrame:
    """
    Method to resample the training data

    Args:
        target (str)
        x_train (pandas.DataFrame)
        up_or_down (str): By default = 'up'
        resampling_perc (float): By default = 1.0

    Returns:
        x_train (pandas.DataFrame)
    """
    majority_label = x_train[target].mode()[0]
    majority_data = x_train[x_train[target] == majority_label]
    minority_data = x_train[x_train[target] != majority_label]

    if resampling_perc > 2.0 or resampling_perc <= 0.01:
        raise Exception(
            f'Invalid value {resampling_perc} for parameter resampling_perc, values must be between 0.01 and 2.00')

    up_or_down = up_or_down.lower().strip()

    if up_or_down == 'up':

        print(f'\t-> Upsampling minority class\n' +
              f'\t\t Minority class will be resampled to {majority_data.shape[0]} number of rows')

        data2resample = minority_data
        n_samples = int(round(majority_data.shape[0] * resampling_perc, 0))
        data2join = majority_data

    elif up_or_down == 'down':

        print(f'\t-> Downsampling majority class\n' +
              f'\t\t Majority class will be resampled to {minority_data.shape[0]} number of rows')

        data2resample = majority_data
        n_samples = int(round(minority_data.shape[0] * resampling_perc, 0))
        data2join = minority_data

    else:
        raise Exception(f'Invalid value {up_or_down} for variable up_or_down. Valid values are ["up","down"]')

    resampled_data = resample(
        data2resample,
        replace=True,
        n_samples=n_samples,
        random_state=1234
    )

    x_train = concat([resampled_data, data2join])

    print(f'\n\t\tNew proportion of targets: {x_train[target].value_counts(normalize=True).to_dict()}\n')

    return x_train
