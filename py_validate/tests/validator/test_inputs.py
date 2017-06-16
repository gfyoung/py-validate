"""
Unittests for the input validator decorator.
"""

from py_validate.validator import validate_inputs
from py_validate.tests import assert_raises

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


@validate_inputs(a="even")
def operate_only_even_two(a):
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


@validate_inputs(a="odd")
def operate_only_odd_two(a):
    return a + 1


@validate_inputs(a=2)
def operate_invalid_check(a):
    return a + 1


@validate_inputs(a="number")
def increment_number(a):
    return a + 1


@validate_inputs(a="integer")
def decrement_number(a):
    return a - 1


def test_valid():
    # The types are correct.
    assert increment(1) == 2
    assert operate_only_odd(7) == -2
    assert operate_only_odd_two(7) == 8

    # These should pass validation.
    assert operate_only_even(2) == -4
    assert increment_no_match(5) == 4
    assert operate_only_even_two(2) == -4

    # These var-args tests shouldn't raise.
    assert operate_var_args(1, 5) == 2
    assert operate_var_args(1, 5, "foo") == 0

    # These kwargs tests shouldn't raise.
    assert operate_kwargs(1) == 2
    assert operate_kwargs(1, b=5, c=2) == 0

    # These shortcut tests shouldn't rise.
    assert increment_number(1) == 2
    assert increment_number(1.5) == 2.5

    assert decrement_number(1) == 0
    assert decrement_number(10) == 9


def test_wrong_number_of_args():
    # We expect Python to handle this for us.
    py3 = sys.version_info >= (3, 0)

    msg = ("takes 1 positional argument" if py3
           else "takes exactly 1 argument")

    assert_raises(TypeError, msg, increment, 1, 1.5)

    msg = ("missing 1 required positional argument" if py3
           else "takes exactly 1 argument")

    assert_raises(TypeError, msg, increment)


def test_invalid_kwargs():
    # We expect Python to handle this for us.
    msg = "got multiple values for argument"
    assert_raises(TypeError, msg, operate_kwargs, 1, a=1)


def test_invalid_type():
    msg = "Validator must either be a shortcut, callable, or type"
    assert_raises(TypeError, msg, operate_invalid_check, 1)

    msg = "Incorrect type for variable"
    assert_raises(TypeError, msg, increment, 1.5)
    assert_raises(TypeError, msg, operate_only_odd, 1.5)
    assert_raises(TypeError, msg, operate_var_args, "foo", 1, 2)
    assert_raises(TypeError, msg, operate_kwargs, a="foo", b=5)

    # No argument matches, so raise whatever
    # error Python is raising natively.
    msg = "unsupported operand type"
    assert_raises(TypeError, msg, increment_no_match, "foo")

    msg = "Expected a number but got"
    assert_raises(TypeError, msg, increment_number, "foo")

    msg = "Expected an integer but got"
    assert_raises(TypeError, msg, decrement_number, "foo")
    assert_raises(TypeError, msg, operate_only_even_two, "foo")

    msg = "Expected an even integer"
    assert_raises(ValueError, msg, operate_only_even_two, 1)

    msg = "Expected an odd integer"
    assert_raises(ValueError, msg, operate_only_odd_two, 2)


def test_failed_validator():
    msg = "Invalid value for variable"
    assert_raises(ValueError, msg, operate_only_even, 3)

    # The validation function itself will fail
    # because the argument has no mod method.
    msg = "unsupported operand type"
    assert_raises(TypeError, msg, operate_only_even, tuple())

    msg = "Odd number expected"
    assert_raises(ValueError, msg, operate_only_odd, 2)
