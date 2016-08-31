""" Helper functions

Most of these functions help validate input values to other functions.
"""
import numbers


def is_non_negative(value, value_label):
    """ Checks if a value is non-negative

    Arguments:
        value: the value to check
        value_label: a name for the value to check

    Raises:
        ValueError: if `value` is not a number or not non-negative
    """
    if not isinstance(value, numbers.Number):
        raise ValueError("`" + value_label + "` must be a number")
    if value < 0:
        raise ValueError("`" + value_label + "` must be non-negative")


def is_positive(value, value_label):
    """ Checks if a value is postive

    Arguments:
        value: the value to check
        value_label: a name for the value to check

    Raises:
        ValueError: if `value` is not a number or not positive
    """
    if not isinstance(value, numbers.Number):
        raise ValueError("`" + value_label + "` must be a number")
    if value <= 0:
        raise ValueError("`" + value_label + "` must be postive")


def is_numeric(value, value_label):
    """ Checks if a value is a number (float or integer)

    Arguments:
        value: the value to check
        value_label: a name for the value to check

    Raises:
        ValueError: if `value` is not a number
    """
    if not isinstance(value, numbers.Number):
        raise ValueError("`" + value_label + "` must be a number")


def is_float(value, value_label):
    """ Checks if a value is a float

    Arguments:
        value: the value to check
        value_label: a name for the value to check

    Raises:
        ValueError: if `value` is not a float
    """
    if not isinstance(value, float):
        raise ValueError("`" + value_label + "` must be a float")


def is_integer(value, value_label):
    """ Checks if a value is an integer

    Arguments:
        value: the value to check
        value_label: a name for the value to check

    Raises:
        ValueError: if `value` is not a integer
    """
    if not isinstance(value, int):
        raise ValueError("`" + value_label + "` must be an integer")


def is_boolean(value, value_label):
    """ Checks if a value is a Boolean

    Arguments:
        value: the value to check
        value_label: a name for the value to check

    Raises:
        ValueError: if `value` is not a Boolean
    """
    if not isinstance(value, bool):
        raise ValueError("`" + value_label + "` must be an Boolean")


def is_integer_min_2(value, value_label):
    """ Checks if a value is an integer greated than 2

    This function will mostly be used for sample size validation.

    Arguments:
        value: the value to check
        value_label: a name for the value to check

    Raises:
        ValueError: if `value` is not a integer or `value` is less than 2.
    """
    if not isinstance(value, int):
        raise ValueError("`" + value_label + "` must be an integer")
    if value < 2:
        raise ValueError("`" + value_label + "` must be greated than 2")


def is_in_0_1(value, value_label):
    """ Checks if a value is in (0, 1)

    Arguments:
        value: the value to check
        value_label: a name for the value to check

    Raises:
        ValueError: if `value` is not in (0, 1)
    """
    is_float(value, value_label)
    if value >= 1 or value <= 0:
        raise ValueError("`" + value_label + "` must in (0, 1)")
