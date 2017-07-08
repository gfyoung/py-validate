"""
Top-level directory for all of py_validate's tests.

This is also the place where any test helpers can be stored.
"""

import pytest


def assert_raises(exc, msg, f, *args, **kwargs):
    """
    Wrapper around pytest's raises function.

    Checks that the expected Exception is raised. However, it
    also provides a nice, more compact way, of checking that
    a particular error message is also provided (if provided
    in the function call).

    Parameters
    ----------
    exc: type
        The Exception class to check for.

    msg: str or None
        The regex to check, if provided.

    f: callable
        The function that we are calling.
    """

    with pytest.raises(exc) as exc_info:
        f(*args, **kwargs)

    if msg is not None:
        exc_info.match(msg)
