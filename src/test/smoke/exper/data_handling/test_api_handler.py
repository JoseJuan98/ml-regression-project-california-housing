# -*- coding: utf-8 -*-
"""Test ApiHandler class."""
import pathlib

import pytest

from exper.data_handling import ApiHandler
from test.smoke.conftest import get_current_config


# @pytest.mark.parametrize("config", [get_current_config()])
def test_api_handler_data_fetching(config):
    """Test API handler fetching data to test it works."""

    data = ApiHandler.load_data(file_path=config.data.raw_data_file, url=config.data.data_url)

    assert data is not None, "No data loaded"
    assert not data.empty, "Data is empty"
