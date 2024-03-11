# -*- coding: utf-8 -*-
"""
Date: 02/2023
Version: 1.0
Author: (I) Jose Pena
Website: https://github.com/JoseJuan98

Utils
========

Utils for pipelines

"""
import numpy
import pandas

from scipy.special import inv_boxcox
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


def rmse(y_true, y_pred):
    return numpy.sqrt(mean_squared_error(y_true, y_pred))


def evaluate_metrics(y_true, y_pred, lmbda: float, precision: int = 4) -> dict:
    """

    Args:
        y_true: array with the evaluation set labels
        y_pred: array with the predictions
        precision: number of decimal numbers

    Returns:
        dict: per model
                - MSE: penalizes big errors
                - RMSE: standardize unit errors
                - R2: proportion of variance (0,1) - The bigger better
                - MAE: average of errors
    """
    y_pred = inv_boxcox(y_pred, lmbda)

    # if not all outliers were cleaned, it can generate NaN values
    # so, for the evaluation they get remove from y_pred and y_true
    y_pred = pandas.DataFrame(y_pred)
    y_pred.columns = ["col"]
    y_pred.index = y_true.index
    index_nan = y_pred[y_pred["col"].isnull()].index.to_list()
    y_pred = y_pred.drop(index=index_nan)
    y_true = y_true.drop(index=index_nan)

    mse = mean_squared_error(y_true=y_true, y_pred=y_pred, squared=False)
    rmse = numpy.sqrt(mse)
    r2 = r2_score(y_true=y_true, y_pred=y_pred)
    mae = mean_absolute_error(y_true=y_true, y_pred=y_pred)

    return {
        "MSE": round(mse, precision),
        "RMSE": round(rmse, precision),
        "R2": round(r2, precision),
        "MAE": round(mae, precision),
    }
