# -*- coding: utf-8 -*-
"""DataHanlder abstract class."""

from abc import ABC, abstractmethod

import pandas


class DataHandler(ABC):
    """DataHandler abstract class."""

    @abstractmethod
    def load_data(self, file_path_or_url: str) -> pandas.DataFrame:
        """Load data from file path or url"""
