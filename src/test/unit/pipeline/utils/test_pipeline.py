# -*- coding: utf-8 -*-
"""Test Pipeline Utils.

Tests exper utilities
"""
import argparse
import unittest
import pathlib

import pytest

from pipeline.utils import get_file_extension, load_artifacts
from src.test.conftest import message_error_expected


@pytest.mark.parametrize(
    "filepath,expected",
    [
        ("path/file.csv", ".csv"),
        ("/path/file.joblib", ".joblib"),
        ("file.joblib", ".joblib"),
        ("./file.joblib", ".joblib"),
        (pathlib.Path("path/file.csv"), ".csv"),
        (pathlib.Path("/path/file.joblib"), ".joblib"),
        (pathlib.Path("file.joblib"), ".joblib"),
        (pathlib.Path("./file.joblib"), ".joblib"),
    ],
)
def test_get_file_extension(filepath, expected):
    file_extension = get_file_extension(filepath=filepath)
    assert file_extension == expected, message_error_expected(
        input_value=filepath, expected=expected, error_value=file_extension
    )


def test_load_artifacts_wrong_file_ext():
    test_args = argparse.Namespace(input_file="file.wrong_extension")
    with pytest.raises(KeyError):
        load_artifacts(args=test_args)


@pytest.mark.parametrize("args, expected", [(argparse.Namespace(), {})])
def test_load_artifacts(args, expected):
    test_args = argparse.Namespace(input_file="file.wrong_extension")
    with pytest.raises(KeyError):
        load_artifacts(args=test_args)


if __name__ == "__main__":
    unittest.main()
