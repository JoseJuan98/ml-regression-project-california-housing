# -*- coding: utf-8 -*-
"""Model definition for experiments."""

from typing import Union, Type, Dict, List
from dataclasses import dataclass
from abc import ABC, abstractmethod


import keras
import numpy
import sklearn


@dataclass
class Metrics:
    """Metrics definition.

    Args:
        train (dict): Dictionary with the training metrics, e.g., {'mse': [0.3, 1.1, ...], 'rmse': [...]}
        test (dict): Dictionary with the test metrics, e.g., {'mse': [1, 1.3, ...], 'rmse': [1, ...]}
    """

    train: Dict[str, Union[List[float], numpy.ndarray]]
    test: Dict[str, Union[List[float], numpy.ndarray]]


class Model(ABC):
    """Abstract class for models.

    Attributes:
        model (sklearn.base, keras.Model): model object
        metrics (Metrics): metrics per iteration during training
    """

    name: str = ""

    def __init__(self, model: Union[Type[sklearn.base], Type[keras.Model]]):
        """Initialize the model.

        Args:
            model (sklearn.base, keras.Model): model object
        """
        self.model = model
        self.metrics = Metrics(train=dict(), test=dict())

    @abstractmethod
    def fit(self, x, y):
        pass

    @abstractmethod
    def predict(self, x):
        pass
