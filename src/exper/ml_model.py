# -*- coding: utf-8 -*-
"""Model definition for experiments."""
from abc import ABC, abstractmethod


class MlModel(ABC):

    @abstractmethod
    def fit(self):
        pass

    @abstractmethod
    def predict(self):
        pass
