# -*- coding: utf-8 -*-
"""California Census data experiment with Neural Network and Linear Regression."""
import os
from typing import Type

import numpy
from scipy import stats
from matplotlib import pyplot

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
        """Visualize all models per metric together in plots."""
        # {metrics: {model: {train: ..., test: ...}}}
        metrics = self.metrics

        set_plotting_style()

        model_names = [model.name for model in self.models]
        for metric in metrics:
            for model_name in model_names:
                pyplot.plot(metrics[metric][model_name]["train"], label=f"{model_name} Train {metric.upper()}")
                pyplot.plot(metrics[metric][model_name]["test"], label=f"{model_name} Test {metric.upper()}")

            pyplot.legend()
            pyplot.title(f"Models {metric.upper()}")
            pyplot.ylabel(metric.upper())
            pyplot.xlabel("Iterations")
            pyplot.savefig(PLOT_DIR / f"models_{metric}.png")
            pyplot.show()

    def hypothesis_testing(self) -> None:
        """Hypothesis Testing."""

        metrics = self.metrics

        print(
            "My hypothesis that simple linear models like linear regression work better compared to complex "
            "non-linear models, like neural networks, in small datasets due to linear patterns. "
            " On a more formal definition the Null and Alternative Hypothesis, being the sample population, u_1 the"
            " performance metrics over iterations of a linear model  and u_2 the performance metrics over iterations of"
            " a neural network."
            "- H_0: u_1 <= u_2 The performance metrics of a linear model are less or equal than the ones of the"
            " neural network."
            "- H_1: u_1 > u_2 The performance metrics of a linear model are higher than the ones of the neural network."
        )

        print("\n\nStatistical tests per metric for rejecting or failing to reject the Null Hypothesis:\n")
        model_names = [model.name for model in self.models]
        alpha = 0.05
        for metric in metrics:
            print(f"T-Test for metric {metric}")
            lr_metrics = metrics[metric][model_names[0]]["test"]
            nn_metrics = metrics[metric][model_names[1]]["test"]

            t_value_1, p_value_1 = stats.ttest_ind(
                a=lr_metrics,
                b=nn_metrics,
            )
            p_value_onetail = p_value_1 / 2
            print(f"t-value: {t_value_1}, p-value: {p_value_1}, p-value-onetail: {p_value_onetail}")
            msg1 = f"Conclusion: since p_value {p_value_1} is " + "{}" + f" than alpha {alpha}"
            msg2 = "{} the null hypothesis that simple linear models performs {} than the complex non-linear ones."

            if p_value_1 < alpha:
                print(msg1.format("less"))
                print(msg2.format("Reject", "less or equal"))

            else:
                print(msg1.format("greater"))
                print(msg2.format("Fail to reject", "greater"))
