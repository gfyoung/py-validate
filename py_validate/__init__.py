from py_validate.validator import *  # noqa

from subprocess import call
from os.path import dirname

__version__ = "0.0.1"


def test():
    """
    Run unit tests on the current py_validate installation.
    """

    directory = dirname(__file__)
    call(["pytest", directory])
