# -*- coding: utf-8 -*-
"""Experiment definition class."""
from abc import ABC, abstractmethod
from typing import Type

import numpy

from exper import Model, Preprocessor
from exper.data_handling import DataHandler


class Experiment(ABC):
    """Experiment Abstrac Class."""

    def __init__(
        self,
        data_handler: Type[DataHandler],
        experiment_name: str,
        preprocesor: Type[Preprocessor],
        models: list[Model],
        param_range: numpy.ndarray | list,
        param_to_experiment: str,
        eval_metrics: str | list[str],
        experiment_description: str = "",
    ) -> None:
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
        """
        self.param_range = param_range
        self.param_to_experiment = param_to_experiment
        self.data_handler = data_handler
        self.experiment_name = experiment_name
        self.experiment_description = experiment_description
        self.preprocesor = preprocesor()
        self.models = models
        self.eval_metrics = eval_metrics

    @property
    def metrics(self):
        metrics = {}

        for metric in self.eval_metrics:
            metrics[metric] = {}

            for model in self.models:
                metrics[metric][model.name] = {}
                metrics[metric][model.name]["train"] = model.metrics.train[metric]
                metrics[metric][model.name]["test"] = model.metrics.test[metric]

        return metrics

    @abstractmethod
    def run(self) -> None:
        """Run the experiment."""

    @abstractmethod
    def visualize_results(self) -> None:
        """Visualize all models per metric together in plots."""

    @abstractmethod
    def hypothesis_testing(self) -> None:
        """Hypothesis Testing."""
