"""
Stacking tests for the decorators i.e. how functions behave when
we start applying more than one of these decorators to a function.
"""

from py_validate.validator import validate_inputs, validate_outputs
from py_validate.backend.shortcuts import NegateFailure
from py_validate.tests import assert_raises


def test_two_inputs():
    @validate_inputs(a=int)
    @validate_inputs(b=int)
    def wrapper(a, b):
        return a + b

    assert wrapper(1, 2) == 3
    assert wrapper(3, 14) == 17
    assert wrapper(*(5, 17)) == 22

    msg = "Incorrect type for variable"
    assert_raises(TypeError, msg, wrapper, "foo", 1)
    assert_raises(TypeError, msg, wrapper, 1, "foo")
    assert_raises(TypeError, msg, wrapper, "foo", "foo")
    assert_raises(TypeError, msg, wrapper, dict(), list())
    assert_raises(TypeError, msg, wrapper, tuple([1, 3]), 4)


def test_output_override():
    @validate_outputs(1)
    @validate_outputs(None, int)
    def wrapper(a):
        if a == 1:
            return a, a
        else:
            return a

    assert wrapper(0) == 0
    assert wrapper(2) == 2

    msg = "Incorrect type for variable"
    assert_raises(TypeError, msg, wrapper, 0.0)
    assert_raises(TypeError, msg, wrapper, "foo")
    assert_raises(TypeError, msg, wrapper, [1, 2])

    msg = "items returned but got"
    assert_raises(ValueError, msg, wrapper, 1)


# TODO: this behavior should be disallowed
def test_two_outputs_append():
    @validate_outputs(None, int)
    @validate_outputs(None, float)
    def wrapper(a):
        if a == 1:
            return float(a), a
        elif a == 0:
            return a, float(a)
        else:
            return float(a), float(a)

    assert wrapper(1) == (1.0, 1)

    msg = "Incorrect type for variable"
    assert_raises(TypeError, msg, wrapper, 0)
    assert_raises(TypeError, msg, wrapper, 2)


def test_input_output():
    @validate_inputs(a=int)
    @validate_outputs(1, float)
    def wrapper(a):
        if a == 0:
            return a
        elif a == 1:
            return a, a
        else:
            return float(a)

    assert wrapper(2) == 2
    assert wrapper(3) == 3

    msg = "Incorrect type for variable"
    assert_raises(TypeError, msg, wrapper, 0)
    assert_raises(TypeError, msg, wrapper, dict())

    msg = "items returned but got"
    assert_raises(ValueError, msg, wrapper, 1)


def test_output_input():
    @validate_outputs(1, float)
    @validate_inputs(a=int)
    def wrapper(a):
        if a == 0:
            return a
        elif a == 1:
            return a, a
        else:
            return float(a)

    assert wrapper(2) == 2
    assert wrapper(3) == 3

    msg = "Incorrect type for variable"
    assert_raises(TypeError, msg, wrapper, 0)
    assert_raises(TypeError, msg, wrapper, {1, 2})

    msg = "items returned but got"
    assert_raises(ValueError, msg, wrapper, 1)


def test_output_negative_count_stack():
    @validate_inputs(a=int)
    @validate_outputs(-1, float)
    def wrapper(a):
        if a == 0:
            return a
        elif a == 1:
            return a, a
        else:
            return float(a)

    assert wrapper(2) == 2
    assert wrapper(3) == 3

    msg = "Incorrect type for variable"
    assert_raises(TypeError, msg, wrapper, 0)
    assert_raises(TypeError, msg, wrapper, [1, 2])

    # We now evaluate the tuple object as is,
    # not the elements of the tuple itself.
    assert_raises(TypeError, msg, wrapper, 1)


def test_invalid_input_stack():
    @validate_inputs(a=1)
    @validate_outputs(1, int)
    def wrapper(a):
        return a - 1

    msg = "Validator must either be a shortcut, callable, or type"
    assert_raises(TypeError, msg, wrapper, 1)


def test_invalid_output_stack():
    @validate_inputs(a=int)
    @validate_outputs(1, 1)
    def wrapper(a):
        return a - 1

    msg = "Validator must either be a shortcut, callable, or type"
    assert_raises(TypeError, msg, wrapper, 1)


def test_input_output_sandwich():
    @validate_inputs(a=int)
    @validate_outputs(1, int)
    @validate_inputs(b=int)
    def wrapper(a, b):
        if a == b:
            return a + b
        elif a > b:
            return float(a + b)
        else:
            return a + b, a + b

    assert wrapper(1, 1) == 2

    msg = "items returned but got"
    assert_raises(ValueError, msg, wrapper, 0, 1)

    msg = "Incorrect type for variable"
    assert_raises(TypeError, msg, wrapper, 1, 0)
    assert_raises(TypeError, msg, wrapper, "foo", 1)
    assert_raises(TypeError, msg, wrapper, 1, "foo")
    assert_raises(TypeError, msg, wrapper, "foo", "foo")
    assert_raises(TypeError, msg, wrapper, [1, 2], {1, 2})


def test_shortcuts_stack():
    @validate_inputs(a="odd")
    @validate_outputs(1, "even")
    def wrapper(a):
        if a == -1:
            return a, a
        elif a == 1:
            return a
        else:
            return 2 * a

    assert wrapper(3) == 6
    assert wrapper(5) == 10

    msg = "items returned but got"
    assert_raises(ValueError, msg, wrapper, -1)

    msg = "Expected an odd integer"
    assert_raises(ValueError, msg, wrapper, 0)

    msg = "Expected an even integer"
    assert_raises(ValueError, msg, wrapper, 1)


def test_negate_stack():
    @validate_inputs(a="integer")
    @validate_inputs(b="~number")
    def wrapper(a, b):
        return a * b

    assert wrapper(2, "bar") == "barbar"
    assert wrapper(3, [1, 2]) == [1, 2, 1, 2, 1, 2]

    msg = "Expected an integer"
    assert_raises(TypeError, msg, wrapper, "foo", "bar")
    assert_raises(TypeError, msg, wrapper, [1, 2, 3], "bar")

    msg = "'number' passed when it shouldn't have"
    assert_raises(NegateFailure, msg, wrapper, 5, 5)
    assert_raises(NegateFailure, msg, wrapper, 5, 12.1)
