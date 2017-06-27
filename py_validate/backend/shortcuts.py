from .helpers import FrozenDict

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


# For internal use only. The only thing that should
# access this is "get_shortcut."
mappings = FrozenDict(odd=check_odd, even=check_even,
                      number=check_number, integer=check_integer)


def get_shortcut(shortcut):
    """
    Get the function associated with a particular shortcut.

    Parameters
    ----------
    shortcut : str
        The shortcut name associated with a function.

    Returns
    -------
    shortcut_func : callable
        The associated function with a shortcut.

    Raises
    ------
    ValueError : an invalid shortcut name was provided.
    """

    shortcut_func = mappings.get(shortcut)

    if shortcut_func is None:
        msg = "Unknown shortcut: '{shortcut}'"
        raise ValueError(msg.format(shortcut=shortcut))

    return shortcut_func


class NegateFailure(Exception):
    """
    Exception class for when a validation function passes when it shouldn't.
    """

    pass


class NegateShortcut(object):

    def __init__(self, shortcut):
        self.shortcut = shortcut
        self.func = get_shortcut(shortcut)
        self.msg = ("Validation for '{shortcut}' "
                    "passed when it shouldn't have")

    def __call__(self, x):
        try:
            self.func(x)
            raise NegateFailure(self.msg.format(shortcut=self.shortcut))
        except NegateFailure:
            raise
        except (TypeError, ValueError):
            pass
