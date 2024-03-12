# -*- coding: utf-8 -*-
"""Preprocessing class definition for experiments."""
from abc import ABC, abstractmethod


class MlPreprocessor(ABC):

    @abstractmethod
    def fit(self):
        pass

    @abstractmethod
    def predict(self):
        pass
