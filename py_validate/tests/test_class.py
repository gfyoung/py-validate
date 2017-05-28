"""
Unittests for fuzzy inputs to the `_ValidatedFunction` class.
"""

from py_validate.validator import _ValidatedFunction

import pytest


def test_input_not_callable():
    matcher = "Invalid function parameter provided"

    with pytest.raises(ValueError) as exc_info:
        _ValidatedFunction(2)

    exc_info.match(matcher)

    with pytest.raises(ValueError) as exc_info:
        _ValidatedFunction([1, 2, 3])

    exc_info.match(matcher)

    with pytest.raises(ValueError) as exc_info:
        _ValidatedFunction({1: 2, 4: 5})

    exc_info.match(matcher)


def test_input_wrong_callable():
    matcher = "Invalid function parameter provided"

    class CallableClassNoCode(object):
        def __call__(self):
            pass

    with pytest.raises(ValueError) as exc_info:
        _ValidatedFunction(CallableClassNoCode())

    exc_info.match(matcher)

    class CallableClassNoCoVarnames(object):
        def __call__(self):
            pass

        @property
        def __code__(self):
            return "foo"

    with pytest.raises(ValueError) as exc_info:
        _ValidatedFunction(CallableClassNoCoVarnames())

    exc_info.match(matcher)


def test_input_bad_exp_len():
    validator = _ValidatedFunction(lambda x: x + 1)
    matcher = "Expected an integer for expected output length"

    with pytest.raises(TypeError) as exc_info:
        validator.update_exp_output_len("foo")

    exc_info.match(matcher)
