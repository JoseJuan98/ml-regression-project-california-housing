# -*- coding: utf-8 -*-
"""California Census data experiment with Neural Network and Linear Regression."""
import os
from typing import Type

import numpy

from matplotlib import pyplot, pyplot as plt

from exper import Experiment, Preprocessor, Model
from exper.utils.plotting import set_plotting_style
from exper.constant import HOUSING_DATA_URL, RAW_DATA_FILE, target, PLOT_DIR
from exper.data_handling import ApiHandler, DataHandler
from .california_preprocessor import CaliforniaPreprocessor


class LRvsNNExperiment(Experiment):

    def __init__(
        self,
        data_handler: Type[DataHandler],
        preprocesor: Type[Preprocessor],
        experiment_name: str,
        models: list[Model],
        param_range: numpy.ndarray | list,
        param_to_experiment: str,
        eval_metrics: str | list[str],
        test_size: float = 0.3,
        experiment_description: str = "",
    ):
        """Initialize the experiment.

        Args:
            experiment_name (str): experiment name.
            experiment_description (str): experiment descriptions.
            data_handler (DataHandler): data handler to get the data from
            preprocesor (Preprocessor): preprocessor shared between the models to transform the data.
            models (list[Model]): list of models to be used for training and metrics gathering.
            param_range (list | numpy.ndarray): range of values to be used for experimenting
                with `param_to_experiment
            param_to_experiment (str): parameter to experiment with
            eval_metrics (str | list[str]): metrics to used for evaluation
            test_size (optional, float): By default 0.3. Percentage of data to be used for the test set.
                0 > test_size > 1.

        Raises:
            ValueError: if 0 > test_size > 1
        """
        if 0 > test_size > 1:
            raise ValueError("test_size is a percentage belonging to [0,1]")

        super().__init__(
            experiment_name=experiment_name,
            models=models,
            experiment_description=experiment_description,
            preprocesor=preprocesor,
            data_handler=data_handler,
            param_range=param_range,
            param_to_experiment=param_to_experiment,
            eval_metrics=eval_metrics,
        )

        self.test_size = test_size

    def run(self) -> None:
        """Run the experiment."""

        # get the data
        data = self.data_handler.load_data(file_path=RAW_DATA_FILE, url=HOUSING_DATA_URL)

        # the models should handle the split between test, train and validation
        x_train_test = self.preprocesor.preprocess(data=data, transform_data=True)

        print(f"\nx_train transformed:\n{x_train_test.head().to_string()}")

        # train models
        for model in self.models:
            model.fit(
                x=x_train_test,
                y=data[target],
                param_range=self.param_range,
                param=self.param_to_experiment,
                eval_metrics=self.eval_metrics,
                test_size=self.test_size,
            )

    def visualize_results(self):

        # {metrics: {model: {train: ..., test: ...}}}
        metrics = self.metrics

        set_plotting_style()

        model_names = [model.name for model in self.models]
        for metric in metrics:
            for model_name in model_names:
                pyplot.plot(metrics[metric][model_name]["train"], label=f"{model_name} Train {metric.upper()}")
                pyplot.plot(metrics[metric][model_name]["test"], label=f"{model_name} Train {metric.upper()}")

            pyplot.legend()
            pyplot.title(f"Models {metric.upper()}")
            pyplot.ylabel(metric.upper())
            pyplot.xlabel("Iterations")
            pyplot.savefig(PLOT_DIR / f"models_{metric}.png")
            pyplot.show()


if __name__ == "__main__":
    experiment = LRvsNNExperiment(
        experiment_name="LR vs NN Experiment",
        experiment_description="",
        data_handler=ApiHandler,
        models=[],
        preprocesor=CaliforniaPreprocessor,
        param_range=numpy.arange(1, 101, 1),
        param_to_experiment="iterations",
        eval_metrics=["rmse", "mse", "mae"],
    )

    experiment.run()
