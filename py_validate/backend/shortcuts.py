import numbers


def check_number(x):
    """
    Check if a variable is a number.

    Parameters
    ----------
    x : object
        The variable to check.

    Raises
    ------
    TypeError : the variable was not a number.
    """

    act_type = type(x).__name__
    msg = "Expected a number but got: '{act_type}'".format(act_type=act_type)

    if not (isinstance(x, numbers.Number) and not isinstance(x, bool)):
        raise TypeError(msg)


def check_integer(x):
    """
    Check if a variable is an integer.

    Parameters
    ----------
    x : object
        The variable to check.

    Raises
    ------
    TypeError : the variable was not an integer.
    """

    act_type = type(x).__name__
    msg = "Expected an integer but got: '{act_type}'".format(act_type=act_type)

    if not (isinstance(x, numbers.Integral) and not isinstance(x, bool)):
        raise TypeError(msg)


def check_even(x):
    """
    Check if a variable is an even number.

    Parameters
    ----------
    x : object
        The variable to check.

    Raises
    ------
    TypeError : the variable was not an even number.
    """

    check_integer(x)

    if x % 2 != 0:
        raise ValueError("Expected an even integer")


def check_odd(x):
    """
    Check if a variable is an odd number.

    Parameters
    ----------
    x : object
        The variable to check.

    Raises
    ------
    TypeError : the variable was not an odd number.
    """

    check_integer(x)

    if x % 2 != 1:
        raise ValueError("Expected an odd integer")


mappings = {
    "odd": check_odd,
    "even": check_even,
    "number": check_number,
    "integer": check_integer,
}
