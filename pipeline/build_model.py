# -*- coding: utf-8 -*-
"""
Date: 02/2023
Version: 1.0
Author: (I) Jose Pena
Website: https://github.com/JoseJuan98


Title
=====

...
"""
import argparse
import logging
import os
from typing import Dict

import joblib
import pandas
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline

from pipeline.utils import pipe_args, parse_args, get_preprocessor

# from onnxmltools import convert_sklearn
# from onnxmltools.convert.common.data_types import StringTensorType, FloatTensorType, Int64TensorType

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


# def dataframe2onnx_schema(dataframe: pandas.DataFrame, drop=None) -> list:
#     inputs = []
#
#     for k, v in zip(dataframe.columns, dataframe.dtypes):
#         if drop is not None and k in drop:
#             continue
#         if v in ['int', 'int32', 'int64']:
#             t = Int64TensorType([None, 1])
#         elif v in ['float', 'float32', 'float64']:
#             t = FloatTensorType([None, 1])
#         else:
#             t = StringTensorType([None, 1])
#         inputs.append((k, t))
#     return inputs


@pipe_args
def modelling(artifacts: Dict,
              args: argparse.Namespace) -> Dict:
    """
    Train and return a model trained with train_set

    Args:
        artifacts:
        args:

    Returns:

    """
    train_set: pandas.DataFrame = artifacts['train_set']
    test_set: pandas.DataFrame = artifacts['test_set']

    # Extract target
    x_train = train_set.drop('target', axis=1)
    y_train = train_set.pop('target')

    # Pipelines definition
    preprocessor = get_preprocessor(
        categorical_columns=train_set.select_dtypes(include=['O', 'object']).columns.tolist(),
        numerical_columns=train_set.select_dtypes(include='number').columns.tolist()
    )

    # Model and grid definition
    model = GridSearchCV(
        estimator=LogisticRegression(n_jobs=-1, random_state=42, max_iter=1000),
        param_grid={
            'solver': ['saga'],
            'penalty': ['elasticnet'],
            'l1_ratio': [x / 10 for x in range(11)],
            'C': [10, 1.0, 0.1]
        },
        cv=5,
        scoring='roc_auc',
        n_jobs=-1,
        verbose=1
    )

    classifier_pipeline = Pipeline([('preprocessor', preprocessor),
                                    ('classifier', model)],
                                   verbose=True)

    classifier_pipeline.fit(X=x_train, y=y_train)

    # Store serialized data
    joblib.dump(value={"train_set": train_set,
                       "test_set": test_set},
                filename=os.path.join(args.artifact_path, "data_sets.joblib")
                )

    return {"classifier_pipeline": classifier_pipeline}


if __name__ == '__main__':
    # Example of usage of the parameters to run it locally:
    #  --artifact-path="../bin" --step-name="Modelling" --env="local" --input-file="feature_prep.joblib"
    #  --output-file="train_artifacts.joblib"
    args = parse_args(return_parser=False)

    modelling(args=args, logger=logger)