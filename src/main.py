# /!\ ++++++++++++++++++++++++++++++ FINAL +++++++++++++++++++++++++++++++
# FIXME: put requirements/ , setup.py, environment.yaml into src/ and remove LICENSE from setup.py
#       test that the lib setup works

# -*- coding: utf-8 -*-
"""Main script with the solution of the exercises."""
import keras
import numpy
import pandas

from sklearn.linear_model import Lasso

from exper.constant import RAW_DATA_FILE, HOUSING_DATA_URL
from exper.data_handling import ApiHandler

from src.analysis.exploratory_data_analysis import exploratory_data_analysis
from src.analysis.exploratory_feature_engineering import exploratory_feature_engineering

from src.experiments.california_preprocessor import CaliforniaPreprocessor
from src.experiments.lr_vs_nn_experiment import LRvsNNExperiment
from src.experiments.linear_regression import LinearRegress
from src.experiments.neural_network import NeuralNetwork

# to show all columns without cuts
pandas.set_option("display.max_columns", None)


def section_msg(msg: str):
    """Print the title message for a task."""
    print(f"\n\n{msg:_^100}\n\n")


def main() -> None:
    """Main function."""

    housing_data = ApiHandler.load_data(file_path=RAW_DATA_FILE, url=HOUSING_DATA_URL)

    section_msg(" 1. Exploratory Data Analysis ")
    # exploratory_data_analysis(data=housing_data)

    section_msg(" 2. Data Cleaning and Feature Engineering ")
    exploratory_feature_engineering(data=housing_data)

    section_msg(" 3. Experimenting with models ")
    # Model definitions

    # The sklearn model Lasso was choosen instead of LinearRegression because LinearRegression
    # doesn't have the parameter max_iters to iterate for
    lr_model = LinearRegress(model=Lasso())
    nn_model = NeuralNetwork(model=keras.Sequential)

    experiment = LRvsNNExperiment(
        experiment_name="LR vs NN Experiment",
        experiment_description="",
        data_handler=ApiHandler,
        models=[lr_model, nn_model],
        preprocesor=CaliforniaPreprocessor,
        param_range=numpy.arange(1, 100, 1),
        param_to_experiment="iterations",
        eval_metrics=["rmse", "mse", "mae"],
    )

    # run experiment
    experiment.run()

    # visualize experiment results
    experiment.visualize_results()

    section_msg(" 4. Hypothesis testing ")
    experiment.hypothesis_testing()


if __name__ == "__main__":
    main()
