# -*- coding: utf-8 -*-
"""Model definition for experiments."""

from abc import abstractmethod

import numpy
import pandas

from exper import Model
from exper.model import Metrics


class Regressor(Model):
    """Abstract class for regressors.

    Attributes:
        model (sklearn.base, keras.Model): model object
        metrics (Metrics): metrics per iteration during training
    """

    @abstractmethod
    def predict_proba(
        self, x: numpy.ndarray | pandas.DataFrame | pandas.Series
    ) -> numpy.ndarray | pandas.DataFrame | pandas.Series:
        """Predict probabilities of the given input features.

        Args:
            x (numpy.ndarray | pandas.DataFrame | pandas.Series): input features

        Returns:
            numpy.ndarray | pandas.DataFrame | pandas.Series: predictions with a probability
                belonging to [0.0, 1.0]
        """
        pass
