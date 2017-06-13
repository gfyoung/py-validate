from numbers import Number


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

    if not (isinstance(x, Number) and not isinstance(x, bool)):
        raise TypeError(msg)


mappings = {
    "number": check_number
}
