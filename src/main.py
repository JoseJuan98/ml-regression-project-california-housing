# /!\ ++++++++++++++++++++++++++++++ FINAL +++++++++++++++++++++++++++++++
# FIXME: put requirements/ , setup.py, environment.yaml into src/ and remove LICENSE from setup.py
#       test that the lib setup works

# -*- coding: utf-8 -*-
"""Main script with the solution of the exercises."""
import pandas

from exper.contant import RAW_DATA_FILE, HOUSING_DATA_URL
from exper.data_handling import ApiHandler
from src.analysis.data_summary import data_summary

# to show all columns without cuts
pandas.set_option("display.max_columns", None)


def section_msg(msg: str):
    """Print the title message for a task."""
    print(f"\n\n{msg:_^100}\n\n")


def main() -> None:
    """Main function."""

    housing_data = ApiHandler.load_data(file_path=RAW_DATA_FILE, url=HOUSING_DATA_URL)

    section_msg(" 1. Data Summary ")
    data_summary(data=housing_data)

    section_msg(" 2. Data Cleaning and Feature Engineering ")
    # TODO

    section_msg(" 3. Modeling ")
    # TODO

    section_msg(" 4. Hypothesis testing ")
    # TODO


if __name__ == "__main__":
    main()
