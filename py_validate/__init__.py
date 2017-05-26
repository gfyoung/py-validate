from py_validate.validator import *  # noqa

from subprocess import call
from os.path import dirname


def test():
    """
    Run unit tests on the current py_validate installation.
    """

    directory = dirname(__file__)
    call(["pytest", directory])
