import logging

from pandas import DataFrame, NA, concat
from sklearn.pipeline import Pipeline

from src.utils import logger, TARGET


def remove_outliers_iqr(dataframe: DataFrame, column: str, whisker_width: float = 1.5) -> DataFrame:
    """
    Method to remove outliers from a dataframe by column, including optional whiskers, removing rows
     for which the column value are less than Q1-1.5IQR or greater than Q3+1.5IQR.

    Args:
        dataframe (`:obj:pd.DataFrame`): A pandas dataframe to subset
        column (str): Name of the column to calculate the subset from.
        whisker_width (float): Optional, loosen the IQR filter by a factor of `whisker_width` * IQR.

    Returns:
        (`:obj:pd.DataFrame`): Filtered dataframe
    """
    # Calculate Q1, Q2 and IQR
    q1 = dataframe[column].quantile(0.25)
    q3 = dataframe[column].quantile(0.75)
    iqr = q3 - q1
    # Apply filter with respect to IQR, including optional whiskers
    return dataframe.loc[
        (dataframe[column] >= q1 - whisker_width * iqr) & (dataframe[column] <= q3 + whisker_width * iqr)]


def prepare_data(data: DataFrame, target: str, verbose: bool = False) -> DataFrame:
    """

    Args:
        verbose (bool): if True it will print the messages, if not it won't
        target (str): name of the target variable
        data (pandas.DataFrame): raw data to be prepared

    Returns:
        pandas.DataFrame: prepared data
    """
    if verbose:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.ERROR)

    logger.info(f"{'':_^30} Preparing Data {'':_^30}")

    from scipy.stats import boxcox
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import OneHotEncoder, MinMaxScaler

    # Normalizing target variable
    old_skewness = data[target].skew()
    data[target] = DataFrame(boxcox(data.median_house_value)[0])

    logger.info(f"\t-> Target normalization. \n\t\tSkewness: \n"
                f"{'':>30}{'Old':10}: {old_skewness:.4f}. \n"
                f"{'':>30}{'Current':10}: {data[target].skew():.4f}\n"
                f"\n\t-> Handling missing values. \n"
                f"\t\tMissing values of `total_bedrooms`:\n"
                f"{'':>30}{'Before':10}: {data.total_bedrooms.isna().sum()}")

    # Missing values
    imputer = SimpleImputer(missing_values=NA, strategy='mean')
    data.total_bedrooms = imputer.fit_transform(X=data.total_bedrooms.to_numpy().reshape(-1, 1))

    logger.info(f"{'':>30}{'After':10}: {data.total_bedrooms.isna().sum()}"
                f"\n\n\t-> Handling outliers.")

    # Handling outliers
    variables_with_outliers = ["median_income", "total_rooms", "total_bedrooms", "population", "median_income",
                               "housing_median_age", "households"]
    for col in variables_with_outliers:
        data = remove_outliers_iqr(dataframe=data, column=col, whisker_width=1.5)

    # Encoding categorical variables
    logger.info(f"\t-> Encoding categorical variables.")
    categorical_variables = data.select_dtypes('object').columns.to_list()
    cat_encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')
    original_index = data[categorical_variables].index

    new_cat_data = cat_encoder.fit_transform(data[categorical_variables])
    new_cat_columns = cat_encoder.get_feature_names_out().tolist()

    new_cat_data = DataFrame(data=new_cat_data, columns=new_cat_columns)
    new_cat_data.set_index(original_index, inplace=True)
    data = concat([data, new_cat_data], axis=1, join='inner')
    del new_cat_data, original_index
    data.drop(columns=categorical_variables, inplace=True, axis=1)

    # Scaling numerical variables
    logger.info(f"\t-> Scaling continuous variables.\n")
    norm_cols = [col for col in data.columns.tolist() if col not in new_cat_columns + [TARGET]]

    norm_data = MinMaxScaler().fit_transform(data[norm_cols])
    original_index = data[norm_cols].index

    norm_data = DataFrame(data=norm_data, columns=norm_cols)
    norm_data.set_index(original_index, inplace=True)
    data[norm_cols] = norm_data[norm_cols]
    del norm_data, original_index

    return data


def get_processing_pipeline() -> Pipeline:
    """

    Returns:
        Pipeline: pipeline with the data preparation for a ml model
    """
    from sklearn.impute import SimpleImputer

    pipe = Pipeline()

    SimpleImputer(missing_values=NA, strategy='mean')

    return pipe
