#!/usr/bin/env python
"""
Test Pipeline Utils
===================

Tests pipeline utilities

"""
import argparse
import unittest
import pathlib

import pytest

from src.pipeline.utils.pipeline import get_file_extension, load_artifacts
from test.unit.utils import message_error_expected

__author__ = "Jose Pena"
__copyright__ = "Copyright 2007, The CHC Project"
__credits__ = ["Jose Pena"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Jose Pena"
__email__ = "ss@.org"
__status__ = "Production"


@pytest.mark.parametrize("filepath,expected",
                         [("path/file.csv", ".csv"),
                          ("/path/file.joblib", ".joblib"),
                          ("file.joblib", ".joblib"),
                          ("./file.joblib", ".joblib"),
                          (pathlib.Path("path/file.csv"), ".csv"),
                          (pathlib.Path("/path/file.joblib"), ".joblib"),
                          (pathlib.Path("file.joblib"), ".joblib"),
                          (pathlib.Path("./file.joblib"), ".joblib")
                          ])
def test_get_file_extension(filepath, expected):
    file_extension = get_file_extension(filepath=filepath)
    assert file_extension == expected, message_error_expected(input_value=filepath,
                                                              expected=expected,
                                                              error_value=file_extension)


def test_load_artifacts_wrong_file_ext():
    test_args = argparse.Namespace(input_file="file.wrong_extension")
    with pytest.raises(KeyError):
        load_artifacts(args=test_args)


@pytest.mark.parametrize("args, expected",
                         [(argparse.Namespace(), {})])
def test_load_artifacts(args, expected):
    test_args = argparse.Namespace(input_file="file.wrong_extension")
    with pytest.raises(KeyError):
        load_artifacts(args=test_args)


if __name__ == '__main__':
    unittest.main()
