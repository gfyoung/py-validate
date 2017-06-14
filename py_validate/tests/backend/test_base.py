"""
Unittests for fuzzy inputs to the `_ValidatedFunction` class.
"""

from py_validate.backend import ValidatedFunction
from py_validate.tests import assert_raises

import pytest


@pytest.mark.parametrize("invalid", [
    2, [1, 2, 3], {1: 2, 4: 5}
])
def test_input_not_callable(invalid):
    msg = "Invalid function parameter provided"
    assert_raises(ValueError, msg, ValidatedFunction, invalid)


class CallableClassNoCode(object):
    def __call__(self):
        pass


class CallableClassNoCoVarnames(object):
    def __call__(self):
        pass

    @property
    def __code__(self):
        return "foo"


@pytest.mark.parametrize("klass", [
    CallableClassNoCode, CallableClassNoCoVarnames
])
def test_input_wrong_callable(klass):
    msg = "Invalid function parameter provided"
    assert_raises(ValueError, msg, ValidatedFunction, klass())


def test_input_bad_exp_len():
    validator = ValidatedFunction(lambda x: x + 1)
    msg = "Expected an integer for expected output length"
    assert_raises(TypeError, msg, validator.update_exp_output_len, "foo")
