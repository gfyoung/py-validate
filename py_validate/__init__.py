from py_validate.validator import *  # noqa

from subprocess import call
from os.path import dirname

__version__ = "0.0.1"


def test():
    """
    Run unit tests on the current py_validate installation.
    """

    try:
        import pytest  # noqa
    except ImportError:
        raise ImportError("pytest not found. Please install "
                          "with `pip install pytest`")

    directory = dirname(__file__)
    call(["pytest", directory])
