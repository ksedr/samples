#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Problem 2.

import numpy as np
import pandas as pd


def replace_missing(input_list):
    """Replace all missing values of a given list with:
     - the mean of the values in that list - in case of numeric lists,
     - the modal value (if one exists) - otherwise.

     Modal value is a value that appears most often (at least 2 times) in a set of data.
     If there is no unique modal value in the input list than one (of the modal values) is selected at random.

    Args:
        input_list (list): A list of hashable objects (may contain missing values).

    Returns:
        The input list with missing values replaced by the mean (in case of numeric lists)
        or the modal value - if one exists - (otherwise) of that list.

    Examples:
    >>> replace_missing([1])
    [1]
    >>> replace_missing([])
    []
    >>> replace_missing([1, None])
    [1.0, 1.0]
    >>> replace_missing([1, None, 3])
    [1.0, 2.0, 3.0]
    >>> replace_missing([None, -2, 4])
    [1.0, -2.0, 4.0]
    >>> replace_missing(['1', '1', '2'])
    ['1', '1', '2']
    >>> replace_missing(['1', '1', '4', None])
    ['1', '1', '4', '1']
    >>> replace_missing([None, '1', None, '1', None, None])
    ['1', '1', '1', '1', '1', '1']
    >>> replace_missing(['1', '4', '2', None]) # non-numeric vector with no modal value
    ['1', '4', '2', nan]
    """

    data = pd.Series(input_list)
    if np.issubdtype(data.dtype, np.number):
        value = data.mean()
    else:
        value = data.mode()
        if not value.empty:
            value = value[0]
    data = data.fillna(value)
    return data.tolist()


if __name__ == "__main__":
    import doctest

    doctest.testmod()
