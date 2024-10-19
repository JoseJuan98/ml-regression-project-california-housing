# -*- coding: utf-8 -*-
"""Test Exper Config."""

import pytest

from exper import Config


def test_config():

    config_test = Config()

    assert config_test.data is not None, "DataConfig is not being readed properly"
    assert isinstance(config_test.data.desc, str), "DataConfig desc is not being readed properly"


if __name__ == "__main__":
    pytest.main()
