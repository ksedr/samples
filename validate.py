# -*- coding: utf-8 -*-


def validate(expression):
    """Check the validity of parentheses in a mathematical expression

        Args:
            expression: mathematical expression.

        Returns:
            True if parentheses are valid, False otherwise.

        Examples:
        >>> validate("(2 + 4) * 4")
        True
        >>> validate("(4 * 4 - (log20 / 5)")
        False
        >>> validate("3 - (5 * 2))")
        False
        >>> validate("3 + 2x * 5")
        True

    """
    open_parenthesis = "("
    close_parenthesis = ")"

    counter_open = 0

    for s in expression:
        if s == open_parenthesis:
            counter_open += 1
        elif s == close_parenthesis:
            counter_open -= 1
            if counter_open < 0:
                return False
    if counter_open == 0:
        return True
    return False


if __name__ == "__main__":
    import doctest
    doctest.testmod()
