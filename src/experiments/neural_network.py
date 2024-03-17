# -*- coding: utf-8 -*-
"""Linear Regression Exper Model for experimentation."""
from copy import copy
from typing import Union, Type

import keras
import numpy
import pandas
import sklearn

from sklearn.model_selection import train_test_split

from exper import Model


class NeuralNetwork(Model):
    """Linear Regression Model for experimentation.

    Attributes:
        model (sklearn.base, keras.Model): model object
        metrics (Metrics): metrics per iteration during training
    """

    name = "Neural Network"

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
        test_size: float = 0.15,
    ) -> None:
        """Train the model.

        Args:
            x (numpy.ndarray | pandas.DataFrame | pandas.Series): input features
            y (numpy.ndarray | pandas.DataFrame | pandas.Series): target variable
            param_range (list | numpy.ndarray): parameter range to experiment with the same model
            param (str): parameter to vary in the range `param_range`
            eval_metrics (str | list[str]): metrics to calculate the performance of the model
            test_size (optional, float): By default 0.3. Percentage of data to be used for the test set.
                0 > test_size > 1.
        """
        self.param_range = param_range
        self.eval_metrics = eval_metrics
        self.param = param

        self.model = self.model(
            layers=[
                keras.layers.Dense(
                    units=100,
                    activation="relu",
                    kernel_regularizer=keras.regularizers.l2(0.01),
                    input_shape=(x.shape[1],),
                ),
                keras.layers.Dropout(0.3),
                keras.layers.Dense(1000, activation="relu", kernel_regularizer=keras.regularizers.l2(0.1)),
                keras.layers.Dropout(0.3),
                keras.layers.Dense(100, activation="relu", kernel_regularizer=keras.regularizers.l2(0.01)),
                keras.layers.Dropout(0.3),
                keras.layers.Dense(1, activation="sigmoid", kernel_regularizer=keras.regularizers.l2(0.01)),
            ]
        )

        # conver metrics to keras metrics
        metrics_kr = copy(eval_metrics)
        if "rmse" in metrics_kr:
            metrics_kr.remove("rmse")
            metrics_kr.append("root_mean_squared_error")

        if "mse" in metrics_kr:
            metrics_kr.remove("mse")
            metrics_kr.append("mean_squared_error")

        if "mae" in metrics_kr:
            metrics_kr.remove("mae")
            metrics_kr.append("mean_absolute_error")

        self.model.compile(optimizer="adam", loss="mean_squared_error", metrics=metrics_kr, jit_compile=True)

        print(f"Neural Network and gather metrics for each {self.param} ...")

        x_train, x_test, y_train, y_test = train_test_split(
            x,
            y,
            test_size=0.3,
            random_state=42,
        )

        print(
            f"\nx_train shape: {x_train.shape}\nx_test shape: {x_test.shape}\ny_train shape: {y_train.shape}\n"
            f"y_test shape: {y_test.shape}\n"
        )
        print(
            f"x_train:\n{x_train.head().to_string()}\nx_test:\n{x_test.head().to_string()}\ny_train:\n"
            f"{y_train.head().to_string()}\ny_test:\n{y_test.head().to_string()}"
        )

        hist = self.model.fit(x=x_train, y=y_train, validation_data=(x_test, y_test), epochs=self.param_range[-1])

        for metric, keras_metric in zip(self.eval_metrics, metrics_kr):
            self.metrics.train[metric] = hist.history[keras_metric]
            self.metrics.test[metric] = hist.history[f"val_{keras_metric}"]
