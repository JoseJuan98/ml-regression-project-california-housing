# -*- coding: utf-8 -*-
"""California Census data experiment with Neural Network and Linear Regression."""

import pandas

from sklearn.model_selection import train_test_split

from exper import Experiment, Preprocessor, Model
from exper.data_handling import ApiHandler
from exper.constant import HOUSING_DATA_URL, RAW_DATA_FILE, target


class LRvsNNExperiment(Experiment):

    def __init__(
        self, experiment_name: str, models: list[Model], test_size: float = 0.3, experiment_description: str = None
    ):
        """Initialize the experiment.

        Args:
            experiment_name (str): experiment name.
            experiment_description (str): experiment descriptions.
            test_size (optional, float): By default 0.3. Percentage of data to be used for the test set.
                0 > test_size > 1.
            models (list[Model]): list of models to be used for training and metrics gathering.

        Raises:
            ValueError: if 0 > test_size > 1
        """
        if 0 > test_size > 1:
            raise ValueError("test_size is a percentage belonging to [0,1]")

        super().__init__(experiment_name=experiment_name, models=models, experiment_description=experiment_description)

        self.test_size = test_size

    def run(self) -> None:
        """Run the experiment."""

        data = ApiHandler().load_data(file_path=RAW_DATA_FILE, url=HOUSING_DATA_URL)

        # split between train and test set for evaluation
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
            test_size=self.test_size,
            stratify=data["income_category"],
            random_state=42,
        )

        # train models
        for model in self.models:
            model.fit(x=x_train, y=y_train)

        # plot results
        self.visualize_results()
