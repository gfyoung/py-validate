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


mappings = {
    "number": check_number,
    "integer": check_integer,
}
