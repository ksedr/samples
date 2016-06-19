#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Problem 1.

import pandas as pd


def replace_missing_with_mean(input_list):
    """Replace all missing values of a numeric list with the mean of that list.

    Args:
        input_list (list): A list of numbers (may contain missing values).

    Returns:
        The input list with all missing values replaced by the mean of that list.

    Examples:
    >>> replace_missing_with_mean([1])
    [1]
    >>> replace_missing_with_mean([])
    []
    >>> replace_missing_with_mean([1, None])
    [1.0, 1.0]
    >>> replace_missing_with_mean([1, None, 3])
    [1.0, 2.0, 3.0]
    >>> replace_missing_with_mean([None, -2, 3, None])
    [0.5, -2.0, 3.0, 0.5]
    """
    data = pd.Series(input_list)
    value = data.mean(skipna=True)
    data = data.fillna(value)
    return data.tolist()


if __name__ == "__main__":
    import doctest

    doctest.testmod()
