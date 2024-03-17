# -*- coding: utf-8 -*-
"""Preprocessing class definition for experiments."""
from abc import ABC, abstractmethod
from typing import Tuple

import numpy
import pandas


class Preprocessor(ABC):

    @abstractmethod
    def preprocess(
        self, data: pandas.DataFrame, test_size: float = 0.3
    ) -> Tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray, numpy.ndarray]:
        """Preprocess the data and split it into training and test sets.

        Args:
            data (pandas.DataFrame): Data to be preprocessed
            test_size (optional, float): By default 0.3. Percentage of data to be used for the test set.
                0 > test_size > 1.
        """
