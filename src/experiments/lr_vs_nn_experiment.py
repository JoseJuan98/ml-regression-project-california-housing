# -*- coding: utf-8 -*-
"""California Census data experiment with Neural Network and Linear Regression."""
from typing import Type

import numpy
import pandas

from sklearn.model_selection import train_test_split

from exper import Experiment, Preprocessor, Model
from exper.data_handling import ApiHandler, DataHandler
from exper.constant import HOUSING_DATA_URL, RAW_DATA_FILE, target

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

        # split between train and test set for evaluation
        print(
            "The data must be stratified by an important variable, in this case by income category as it was the most"
            " correlated variable. And as the statrified sampling benefits from having few 'stratas'"
            " (portions to stratify), and this variable is continuous, it's better to convert to a categorical one."
        )
        income_category = pandas.cut(
            data["median_income"], bins=[0.0, 1.5, 3.0, 5, 6, data["median_income"].max() + 1.0], labels=[1, 2, 3, 4, 5]
        )

        x_train, x_test, y_train, y_test = train_test_split(
            data.drop(target, axis=1),
            data[target],
            test_size=self.test_size,
            stratify=income_category,
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

        x_train = self.preprocesor.preprocess(data=x_train, transform_data=True)

        print(f"\nx_train transformed:\n{x_train.head().to_string()}")

        # train models
        for model in self.models:
            model.fit(
                x=x_train,
                y=y_train,
                param_range=self.param_range,
                param=self.param_to_experiment,
                eval_metrics=self.eval_metrics,
            )

    def visualize_results(self):

        # {metrics: {model: {train: ..., test: ...}}}
        metrics = self.metrics
        print(metrics)


if __name__ == "__main__":
    experiment = LRvsNNExperiment(
        experiment_name="LR vs NN Experiment",
        experiment_description="",
        data_handler=ApiHandler,
        models=[],
        preprocesor=CaliforniaPreprocessor,
        param_range=numpy.arange(1, 100, 1),
        param_to_experiment="iterations",
        eval_metrics=["rmse"],
    )

    experiment.run()
