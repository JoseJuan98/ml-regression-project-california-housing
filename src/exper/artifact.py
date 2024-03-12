# -*- coding: utf-8 -*-
"""Artifact dataclass for experiments."""


from dataclasses import dataclass

import numpy
import pandas
import sklearn


@dataclass
class Artifact:
    """Artifact dataclass."""

    data: pandas.DataFrame | dict[str, pandas.DataFrame | numpy.ndarray]
    model_pipeline: sklearn.pipeline.Pipeline
    metrics: dict
