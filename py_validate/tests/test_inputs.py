"""
Unittests for the input validator decorator.
"""

from py_validate.validator import validate_inputs

import pytest
import sys


@validate_inputs(a=int)
def increment(a):
    return a + 1


@validate_inputs(a=int)
def increment_no_match(b):
    return b - 1


@validate_inputs(a=lambda x: x % 2 == 0)
def operate_only_even(a):
    return (a / 2) - 5


@validate_inputs(a=int)
def operate_var_args(a, *args):
    if len(args) > 1:
        return a - 1
    else:
        return a + 1


@validate_inputs(a=int)
def operate_kwargs(a, **kwargs):
    if kwargs:
        return a - 1
    else:
        return a + 1


@validate_inputs(a=int)
def validate_odd(a):
    if a % 2 != 1:
        raise ValueError("Odd number expected")


@validate_inputs(a=validate_odd)
def operate_only_odd(a):
    return ((a - 1) / 2) - 5


@validate_inputs(a=2)
def operate_invalid_check(a):
    return a + 1


def test_valid():
    # The types are correct.
    assert increment(1) == 2
    assert operate_only_odd(7) == -2

    # These should pass validation.
    assert operate_only_even(2) == -4
    assert increment_no_match(5) == 4

    # These var-args tests shouldn't raise.
    assert operate_var_args(1, 5) == 2
    assert operate_var_args(1, 5, "foo") == 0

    # These kwargs tests shouldn't raise.
    assert operate_kwargs(1) == 2
    assert operate_kwargs(1, b=5, c=2) == 0


def test_wrong_number_of_args():
    # We expect Python to handle this for us.
    py3 = sys.version_info >= (3, 0)

    with pytest.raises(TypeError) as exc_info:
        increment(1, 1.5)

    if py3:
        matcher = "takes 1 positional argument"
    else:  # Python 2.x
        matcher = "takes exactly 1 argument"

    exc_info.match(matcher)

    with pytest.raises(TypeError) as exc_info:
        increment()

    if py3:
        matcher = "missing 1 required positional argument"
    else:  # Python 2.x
        matcher = "takes exactly 1 argument"

    exc_info.match(matcher)


def test_invalid_kwargs():
    # We expect Python to handle this for us.
    with pytest.raises(TypeError) as exc_info:
        operate_kwargs(1, a=1)

    exc_info.match("got multiple values for argument")


def test_invalid_type():
    matcher = "Validator must either be a callable or type"

    with pytest.raises(TypeError) as exc_info:
        operate_invalid_check(1)

    exc_info.match(matcher)

    matcher = "Incorrect type for variable"

    with pytest.raises(TypeError) as exc_info:
        increment(1.5)

    exc_info.match(matcher)

    with pytest.raises(TypeError) as exc_info:
        operate_only_odd(1.5)

    exc_info.match(matcher)

    with pytest.raises(TypeError) as exc_info:
        operate_var_args("foo", 1, 2)

    exc_info.match(matcher)

    with pytest.raises(TypeError) as exc_info:
        operate_kwargs(a="foo", b=5)

    exc_info.match(matcher)

    # No argument matches, so raise whatever
    # error Python is raising natively.
    with pytest.raises(TypeError) as exc_info:
        increment_no_match("foo")

    exc_info.match("unsupported operand type")


def test_failed_validator():
    with pytest.raises(ValueError) as exc_info:
        operate_only_even(3)

    exc_info.match("Invalid value for variable")

    # The validation function itself will fail
    # because the argument has no mod method.
    with pytest.raises(TypeError) as exc_info:
        operate_only_even(tuple())

    exc_info.match("unsupported operand type")

    with pytest.raises(ValueError) as exc_info:
        operate_only_odd(2)

    exc_info.match("Odd number expected")
