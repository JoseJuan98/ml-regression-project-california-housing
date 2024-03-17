# -*- coding: utf-8 -*-
"""Experiment definition class."""
from abc import ABC, abstractmethod

from exper import Model, Preprocessor


class Experiment(ABC):
    """Experiment"""

    def __init__(
        self, experiment_name: str, preprocesor: Preprocessor, models: list[Model], experiment_description: str = ""
    ) -> None:
        """Initialize the experiment.

        Args:
            experiment_name (str): experiment name.
            experiment_description (str): experiment descriptions.
            preprocesor (Preprocessor): preprocessor shared between the models.
            models (list[Model]): list of models to be used for training and metrics gathering.
        """
        self.experiment_name = experiment_name
        self.experiment_description = experiment_description
        self.preprocesor = preprocesor
        self.models = models

    @property
    def metrics(self):
        metrics = {}
        for model in self.models:
            metrics[model.name] = model.metrics
        return metrics

    @abstractmethod
    def run(self) -> None:
        pass

    def visualize_results(self) -> None:
        raise NotImplementedError
