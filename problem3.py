#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Problem 3.

import numpy as np
import pandas as pd

from problem2 import replace_missing


def read_data(file_path):
    return pd.read_csv(file_path, sep=',', quotechar='"', header=0, encoding='utf-8', index_col=0)


def apply_function_column(data_frame, func):
    # apply the given function to every column in the data frame
    processed_data = data_frame.apply(func, axis=0)
    return processed_data


def convert_column_type(data_frame, column_name, new_dtype):
    data_frame[column_name] = data_frame[column_name].astype(new_dtype)
    return data_frame


def replace_missing_data(data_frame):
    """For every column in the given data frame replace all missing values with:
     - the mean of that column - in case of numeric columns,
     - the modal value of that column (if one exists) - otherwise.

    Args:
        data_frame (pandas.DataFrame): The data frame (may contain missing values) that should be processed.

    Returns:
        The input data frame with missing values in every column replaced by the column mean or modal value.
    """
    data_frame = apply_function_column(data_frame, replace_missing)
    # assert that there are no missing values in the data frame
    assert all(data_frame.notnull()) == True
    return data_frame


if __name__ == "__main__":
    data = read_data("sample.csv")
    print(data.head(15))
    data = replace_missing_data(data)
    # convert values in the birthyr column to int
    data = convert_column_type(data, 'birthyr', np.int32)
    print(data.head(15))
