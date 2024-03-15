# -*- coding: utf-8 -*-
"""Test module for the validation curve."""

import os
import warnings

import numpy

from matplotlib import pyplot
from sklearn.datasets import make_classification
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import ValidationCurveDisplay, validation_curve
from sklearn.utils._plotting import _validate_score_name  # noqa

# we will have convergence issue because of running low numbers of iterations
warnings.filterwarnings("ignore", category=ConvergenceWarning)
os.environ["PYTHONWARNINGS"] = "ignore"


def main() -> None:
    X, y = make_classification(n_samples=1_000, random_state=0)

    param_name = "max_iter"
    param_range = numpy.arange(1, 100, 1)

    negate_score = False
    score_name = None
    scoring = "accuracy"
    score_name = _validate_score_name(score_name, scoring, negate_score)

    train_scores, test_scores = validation_curve(
        estimator=LogisticRegression(solver="liblinear"),
        X=X,
        y=y,
        param_name=param_name,
        param_range=param_range,
        n_jobs=-1,
        scoring=scoring,
    )

    viz = ValidationCurveDisplay(
        param_name="max_iter",
        param_range=param_range,
        train_scores=train_scores,
        test_scores=test_scores,
        score_name=score_name,
    )

    ax = None
    score_type = "both"
    std_display_style = None  # "fill_between"
    line_kw = None
    fill_between_kw = None
    errorbar_kw = None

    disp = viz.plot(
        ax=ax,
        negate_score=negate_score,
        score_type=score_type,
        std_display_style=std_display_style,
        line_kw=line_kw,
        fill_between_kw=fill_between_kw,
        errorbar_kw=errorbar_kw,
    )
    disp.ax_.set_title("Validation Curve for Logistic Regression")
    disp.ax_.set_xlabel("Number of iterations")
    pyplot.legend()
    pyplot.show()


if __name__ == "__main__":
    main()
