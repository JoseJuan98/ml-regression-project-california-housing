# -*- coding: utf-8 -*-
"""Test configuration and fixtures."""

import pytest

from exper import Config


@pytest.fixture(scope="session", name="config")
def get_current_config() -> Config:
    """Get the current project config to test the smoke tests."""
    return Config()
