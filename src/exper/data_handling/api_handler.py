# -*- coding: utf-8 -*-
"""API data Handler module."""
import os
import pathlib
import pandas

from urllib.request import urlretrieve

from .data_handler import DataHandler


class ApiHandler(DataHandler):
    """DataHandler class which uses an API to load the data and store it locally."""

    @classmethod
    def load_data(
        cls, file_path: str = None, url: str = None, force_retrieve: bool = False, *args, **kwargs
    ) -> pandas.DataFrame:
        """Load data from file path or url

        Extracts the data from an url and stores it in a file into the `file_path` or if the file already exists in
        the `file_path` skips the url fetching. Finally, returns a dataframe reading this file.

        Args:
            force_retrieve (optional, bool): By default False. If `force_retrieve=True`: it retrieves data from the url,
                Otherwise it will retrieve from the url only if it wasn't already stored in the file_path.
            url (str): url to extract data from
            file_path (str): location where to store the data in csv format

        Returns:
            DataFrame: data extracted from path or URL
        """
        if isinstance(file_path, str):
            file_path = pathlib.Path(file_path)

        if not file_path.exists() or force_retrieve:
            dir_path = file_path.parent

            if not os.path.isdir(dir_path):
                os.makedirs(dir_path)

            urlretrieve(url=url, filename=file_path)

        return pandas.read_csv(filepath_or_buffer=file_path, low_memory=False)
