# -*- coding: utf-8 -*-
"""DataHandler abstract class."""

from abc import ABC, abstractmethod

import pandas


class DataHandler(ABC):
    """DataHandler abstract class."""

    @classmethod
    @abstractmethod
    def load_data(cls, file_path: str = None, url: str = None, *args, **kwargs) -> pandas.DataFrame:
        """Load data from file path or url

        Args:
            url (str): url to extract data from
            file_path (str): File path to load or save the data
        """
