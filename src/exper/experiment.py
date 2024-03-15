# -*- coding: utf-8 -*-
"""Experiment definition class."""
from abc import ABC, abstractmethod

from exper.model import Model
from exper.preprocessing import Preprocessor


class Experiment(ABC):
    """Experiment"""

    def __init__(
        self, experiment_name: str, experiment_description: str, preprocesor: Preprocessor, model: Model
    ) -> None:
        self.experiment_name = experiment_name
        self.experiment_description = experiment_description
        self.preprocesor = preprocesor
        self.model = model

    @property
    def metrics(self):
        return self.model.metrics

    # @metrics.setter
    # def metrics(self, value):
    #     self.model.metrics = value

    @abstractmethod
    def run(self) -> None:
        pass
