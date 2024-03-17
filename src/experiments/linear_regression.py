# -*- coding: utf-8 -*-
"""Linear Regression Exper Model for experimentation."""
import os
import warnings
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

        # converting the name to the scikit-learn model param
        if param == "iterations":
            param = "max_iter"

        self.param = param

        # conver metrics to scikit-learn metrics
        if "rmse" in eval_metrics:
            eval_metrics.remove("rmse")
            eval_metrics.append("neg_root_mean_squared_error")

        self.eval_metrics = eval_metrics

        # we will have convergence issue because of running low numbers of iterations
        warnings.filterwarnings("ignore", category=ConvergenceWarning)
        os.environ["PYTHONWARNINGS"] = "ignore"

        for metric in self.eval_metrics:
            train_scores, test_scores = validation_curve(
                estimator=self.model,
                X=x,
                y=y,
                param_name=self.param,
                param_range=param_range,
                n_jobs=-1,
                scoring=metric,
            )

            self.metrics.train[metric] = train_scores
            self.metrics.test[metric] = test_scores

    def predict(
        self, x: numpy.ndarray | pandas.DataFrame | pandas.Series
    ) -> numpy.ndarray | pandas.DataFrame | pandas.Series:
        """Predict given input features.

        Args:
            x (numpy.ndarray | pandas.DataFrame | pandas.Series): input features

        Returns:
            numpy.ndarray | pandas.DataFrame | pandas.Series: predictions
        """
        pass
