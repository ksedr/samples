#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Problem 4.

number_to_word = {
    0: "",  # special case
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
    10: "ten",
    11: "eleven",
    12: "twelve",
    13: "thirteen",
    14: "fourteen",
    15: "fifteen",
    16: "sixteen",
    17: "seventeen",
    18: "eighteen",
    19: "nineteen",
    20: "twenty",
    30: "thirty",
    40: "forty",
    50: "fifty",
    60: "sixty",
    70: "seventy",
    80: "eighty",
    90: "ninety",
    100: "hundred",  # instead of onehundred
    1000: "onethousand",
}


def process_tens(n, number_dict):
    units = n % 10
    return number_dict[n - units] + number_dict[units]


def process_hundreds(n, number_dict):
    hundreds, remainder = divmod(n, 100)
    return number_dict[hundreds] + number_dict[100] + process_number(remainder, number_dict)


def process_number(n, number_dict):
    if n in number_dict:
        if n == 100:
            return number_dict[1] + number_dict[100]
        return number_dict[n]

    if n < 100:
        return process_tens(n, number_dict)

    if n < 1000:
        return process_hundreds(n, number_dict)

    raise ValueError("Invalid input")


def count_letters_range(from_val=1, to_val=1000, use_words=False, verbose=False):
    """Count the number of letters needed for writing all numbers in range {from_val,...,to_val} as words.
    Do not count spaces or hyphens.
    Do not use "and" when writing out numbers.
    from_val and to_val have to be in range {1,...,1000} (inclusive)

    Args:
        from_val (int): The lower limit of the range - minimum 1 (default).
        to_val (int): The upper limit of the range (inclusive) - maximum 1000 (default).
        use_words (bool): Indicates if the textual representation of a number should be used
            for intermediate computation (useful for debugging and printing).
        verbose (bool): Indicates whether results of intermediate computations should be displayed or not
            (only when use_words=True).

    Returns:
        The number of letters needed for writing all numbers in range {from_val,...,to_val} as words.

    Raises:
        ValueError: If from_val or to_val are not integers in range {1,...,1000} (inclusive) or from_val > to_val.

    Examples:
    >>> count_letters_range(1, 5)
    19
    >>> count_letters_range(342, 342)
    20
    >>> count_letters_range(115, 115)
    17
    """
    if not (isinstance(from_val, int) and isinstance(to_val, int) and 1 <= from_val <= to_val <= 1000):
        raise ValueError("Invalid input")

    letters_sum = 0
    number_dict = number_to_word
    if not use_words:
        number_dict = {n: len(w) for n, w in number_to_word.items()}
    for n in range(from_val, to_val+1):
        if use_words:
            word = process_number(n, number_dict)
            word_len = len(word)
            if verbose:
                print(n, word, word_len)
        else:
            word_len = process_number(n, number_dict)
        letters_sum += word_len
    return letters_sum


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    print(count_letters_range(use_words=True, verbose=True))
    print(count_letters_range())
