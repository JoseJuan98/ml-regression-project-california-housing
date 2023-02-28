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
import argparse
from typing import Union
from logging import Logger
from datetime import datetime
from time import perf_counter
import subprocess

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


def pipe_args(data_step):
    """Decorator with the parser arguments need for the steps of the pipeline"""

    def execute(args: argparse.Namespace, logger: Logger) -> dict:
        logger.info(f"Starting step {args.step_name}")
        starting_time = perf_counter()

        if args.input_file:
            artifacts = joblib.load(filename=f"{args.artifact_path}/{args.input_file}")
        else:
            artifacts = {}

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
