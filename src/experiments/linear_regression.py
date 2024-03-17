# -*- coding: utf-8 -*-
"""Linear Regression Exper Model for experimentation."""
import os
import warnings
from copy import copy
from typing import Union, Type

import keras
import numpy
import pandas
import sklearn

from sklearn.exceptions import ConvergenceWarning
from sklearn.model_selection import validation_curve

from exper import Model


class LinearRegress(Model):
    """Linear Regression Model for experimentation.

    Attributes:
        model (sklearn.base, keras.Model): model object
        metrics (Metrics): metrics per iteration during training
    """

    name = "Linear Regression"

    def __init__(self, model: Union[Type[sklearn.base], Type[keras.Model]]):
        """Initialize the model.

        Args:
            model (sklearn.base, keras.Model): model object
        """
        super().__init__(model)

    def fit(
        self,
        x: numpy.ndarray | pandas.DataFrame | pandas.Series,
        y: numpy.ndarray | pandas.DataFrame | pandas.Series,
        param_range: list | numpy.ndarray,
        param: str,
        eval_metrics: str | list[str],
        test_size: float = None,  # noqa: it's not used
    ) -> None:
        """Train the model.

        Args:
            x (numpy.ndarray | pandas.DataFrame | pandas.Series): input features
            y (numpy.ndarray | pandas.DataFrame | pandas.Series): target variable
            param_range (list | numpy.ndarray): parameter range to experiment with the same model
            param (str): parameter to vary in the range `param_range`
            eval_metrics (str | list[str]): metrics to calculate the performance of the model
        """
        self.param_range = param_range
        self.eval_metrics = eval_metrics
        self.param = param

        # converting the name to the scikit-learn model param
        if param == "iterations":
            param = "max_iter"

        # convert metrics to scikit-learn metrics for the training
        sk_metrics = copy(self.eval_metrics)
        if "rmse" in sk_metrics:
            sk_metrics.remove("rmse")
            sk_metrics.append("neg_root_mean_squared_error")

        if "mse" in sk_metrics:
            sk_metrics.remove("mse")
            sk_metrics.append("neg_mean_squared_error")

        if "mae" in sk_metrics:
            sk_metrics.remove("mae")
            sk_metrics.append("neg_mean_absolute_error")

        # we will have convergence issue because of running low numbers of iterations
        warnings.filterwarnings("ignore", category=ConvergenceWarning)
        os.environ["PYTHONWARNINGS"] = "ignore"

        print(f"\nTraining Linear Regression models with varying {self.param} ...")
        for metric, sk_metric in zip(self.eval_metrics, sk_metrics):
            # this method makes a shuffle splt between the test and train sets, and further if it's specified the
            # parameter cv then it will be make cross validation from the train set with that amount of splits.
            train_scores, test_scores = validation_curve(
                estimator=self.model,
                X=x,
                y=y,
                param_name=param,
                param_range=param_range,
                n_jobs=-1,
                scoring=sk_metric,
                cv=5,
            )

            # minus scores -> because they are negative values, so it's easier to compare if they are possitive
            # mean(axis=1) -> because it calculates the errors within a confidence interval, so we want the mean of them
            self.metrics.train[metric] = -train_scores.mean(axis=1)
            self.metrics.test[metric] = -test_scores.mean(axis=1)
