# -*- coding: utf-8 -*-
"""California Census data feature engineering and preprocessing for experiments."""
from typing import Tuple

import numpy
import pandas

from sklearn.model_selection import train_test_split

from exper.preprocessing import Preprocessor
from exper.constant import target


class CaliforniaPreprocessor(Preprocessor):
    def preprocess(
        self, data: pandas.DataFrame, test_size: float = 0.2
    ) -> Tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray, numpy.ndarray]:
        """Preprocess the data and split it into training and test sets.

        Args:
            data (pandas.DataFrame): Data to be preprocessed
            test_size (optional, float): By default 0.3. Percentage of data to be used for the test set.
                0 > test_size > 1.

        Raises:
            ValueError: if 0 > test_size > 1
        """
        if 0 > test_size > 1:
            raise ValueError("test_size is a percentage belonging to [0,1]")

        print(
            "The data must be stratified by an important variable, in this case by income category as it was the most"
            " correlated variable. And as the statrified sampling benefits from having few 'stratas'"
            " (portions to stratify), and this variable is continuous, it's better to convert to a categorical one."
        )
        data["income_category"] = pandas.cut(
            data["median_income"], bins=[0.0, 1.5, 3.0, 5, 6, data["median_income"].max() + 1.0], labels=[1, 2, 3, 4, 5]
        )

        x_train, x_test, y_train, y_test = train_test_split(
            data.drop(target, axis=1),
            data[target],
            test_size=test_size,
            stratify=data["income_category"],
            random_state=42,
        )

        return x_train, x_test, y_train, y_test
