# -*- coding: utf-8 -*-
"""Preprocessing class definition for experiments."""
from abc import ABC, abstractmethod

import pandas

from sklearn.compose import ColumnTransformer


class Preprocessor(ABC):

    @abstractmethod
    def preprocess(self, data: pandas.DataFrame, transform_data: bool = True) -> pandas.DataFrame:
        """Preprocess the data

        Args:
            data (pandas.DataFrame): Data to be preprocessed
            transform_data (optional, bool): By default False. If true the data will preprocess. Otherwise, it won't.

        Returns:
            pandas.DataFrame: data preprocessed and transformed if transform_data is True
        """
