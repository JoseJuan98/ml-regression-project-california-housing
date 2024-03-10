# -*- coding: utf-8 -*-
"""
Date: 02/2023
Version: 1.0
Author: (I) Jose Pena
Website: https://github.com/JoseJuan98

Preprocess
==========

Managing the transformation logic and serializing a transformer, train-test set split ...

Script to perform the preparation of feature before training the model.

The correct order of operations should be:

    - Train and test set splitting
    - Feature Selection
    - Data augmentation
    - Data transformations (such as scaling, normalization, or feature engineering) on the training set only.
...

"""
import argparse
import logging

import pandas

from sklearn.model_selection import train_test_split

from src.pipeline.utils import pipe_args, parse_args

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


@pipe_args
def preprocess(artifacts: dict,
               args: argparse.Namespace) -> dict:
    """
    Resample, split, fit a pipeline and transform the data

    Params:
        features (pandas.DataFrame): The original dataset
        args (argparse.Namespace):

    Return:
        pandas.DataFrame: The train dataset
        pandas.DataFrame: The test dataset
    """
    features: pandas.DataFrame = artifacts['data']

    # Split train-test
    train_set, test_set = train_test_split(features,
                                           random_state=42,
                                           stratify=features['target'])

    return {'train_set': train_set,
            'test_set': test_set}


if __name__ == '__main__':
    # If you want to run it locally in your IDE, create the feature group as a csv in the folder bin
    # Then use the following parameters to run it locally:
    # --data-path="../bin" --step-name="Feature Group Extraction" --env="local" --output-file="feature_prep.joblib"
    preprocess(args=parse_args(), logger=logger)