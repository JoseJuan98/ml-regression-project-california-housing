# -*- coding: utf-8 -*-
"""Test module for the validation curve."""

import os
import warnings

import numpy


from matplotlib import pyplot
from sklearn.datasets import make_classification
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import ValidationCurveDisplay

# we will have convergence issue because of running low numbers of iterations
warnings.filterwarnings("ignore", category=ConvergenceWarning)
os.environ["PYTHONWARNINGS"] = "ignore"


def main() -> None:
    X, y = make_classification(n_samples=1_000, random_state=0)

    disp = ValidationCurveDisplay.from_estimator(
        estimator=LogisticRegression(solver="liblinear"),
        X=X,
        y=y,
        param_name="max_iter",
        param_range=numpy.arange(1, 100, 1),
        score_type="both",
        n_jobs=-1,
        score_name="Accuracy",
    )
    disp.ax_.set_title("Validation Curve for Logistic Regression")
    disp.ax_.set_xlabel("Number of iterations")
    pyplot.show()


if __name__ == "__main__":
    main()
