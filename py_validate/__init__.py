from py_validate.validator import *  # noqa

__version__ = "0.1.1"

__doc__ = """
py_validate - Easy-to-use, customizable function validator wrappers in
Python that can be used to check both inputs and outputs of functions.
"""


def test():
    """
    Run unit tests on the current py_validate installation.
    """

    try:
        import pytest  # noqa
    except ImportError:
        raise ImportError("pytest not found. Please install "
                          "with `pip install pytest`")

    from subprocess import call
    from os.path import dirname

    directory = dirname(__file__)
    call(["pytest", directory])
