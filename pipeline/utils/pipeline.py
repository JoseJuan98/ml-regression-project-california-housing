# -*- coding: utf-8 -*-
"""
Date: 02/2023
Version: 1.0
Author: (I) Jose Pena
Website: https://github.com/JoseJuan98

Utils
========

Utils for pipelines

"""
import os
import argparse
import subprocess
import pathlib

from logging import Logger
from datetime import datetime
from time import perf_counter
from typing import Union, Any

import pandas
import joblib


def parse_args(message: str = "",
               return_parser: bool = False
               ) -> Union[argparse.Namespace, argparse.ArgumentParser]:
    """
    Method to parse the arguments need to execute the pipeline step

    Returns:
        argparse.Namespace: object with the arguments used for the pipeline step.
            --step-name
            --artifact-path
            --input-file
            --output-file
    """
    parser = argparse.ArgumentParser(message)

    parser.add_argument("--step-name",
                        dest="step_name",
                        type=str,
                        default="generic",
                        help="Name of the step to be executed")

    parser.add_argument("--artifact-path",
                        dest="artifact_path",
                        type=str,
                        help="Path to work with data")

    parser.add_argument("--input-file",
                        dest="input_file",
                        type=str,
                        help="Filename to extract the data from")

    parser.add_argument("--output-file",
                        dest="output_file",
                        type=str,
                        help="Filename to store the output data")

    parser.add_argument("--requirements",
                        dest="requirements",
                        type=str,
                        help="Extra requirements to install.")

    if return_parser:
        return parser

    args, _ = parser.parse_known_args()

    print(f"Received arguments:\n{args}.\n")

    if args.requirements is not None:
        subprocess.call(f"pip install {args.requirements}".split(" "))

    return args


def get_file_extension(filepath: Union[str, pathlib.Path]) -> str:
    """
    Method to get file extension from a file path

    Args:
        filepath (str, pathlib.Path): file path

    Returns:
        str: file extension
    """
    if isinstance(filepath, str):
        filepath = pathlib.Path(filepath)

    return filepath.suffix


def load_artifacts(args: argparse.Namespace) -> Any:
    """

    Args:
        args (argparse.Namespace): arguments

    Returns:
        Any: object with artifacts
    """
    if not args.input_file:
        return {}

    file_extension = get_file_extension(args.input_file)

    method_to_load = {
        ".joblib": lambda filename: joblib.load(filename=filename),
        ".csv": lambda filename: pandas.read_csv(filepath_or_buffer=filename,
                                                 low_memory=False,
                                                 engine="pyarrow")
    }

    if file_extension not in method_to_load.keys():
        raise KeyError(f"File extension {file_extension} not supported. Try {method_to_load.keys()}")

    return method_to_load[file_extension](filename=os.path.join(args.artifact_path,
                                                                args.input_file))


def pipe_args(data_step):
    """Decorator with the parser arguments need for the steps of the pipeline"""

    def execute(args: argparse.Namespace, logger: Logger) -> dict:
        logger.info(f"Starting step {args.step_name}")
        starting_time = perf_counter()

        artifacts = load_artifacts(args=args)

        artifacts = data_step(artifacts=artifacts, args=args)
        total_time = perf_counter() - starting_time

        if args.output_file is not None:
            joblib.dump(artifacts, filename=f"{args.artifact_path}/{args.output_file}")

        logger.info(f"Finished {args.step_name} Step after {total_time:.4f} seconds.\n\n")

        return data_step

    return execute


def create_summary(dataframe: pandas.DataFrame) -> dict:
    """

    Args:
        dataframe:

    Returns:

    """
    return {'date': datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"),
            'n_samples': dataframe.shape[0],
            'n_features': dataframe.shape[1],
            '%nan_values': round((dataframe.isna().sum().sum() / (dataframe.shape[0] * dataframe.shape[1])) * 100, 2),
            'prop_target': dict(
                round(dataframe['survived'].value_counts(normalize=True, dropna=False), 3)),
            'features': dataframe.columns.tolist()
            }
