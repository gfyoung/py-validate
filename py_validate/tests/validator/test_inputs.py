"""
Unittests for the input validator decorator.
"""

from py_validate.validator import validate_inputs
from py_validate.tests import assert_raises

import sys


def f(a):
    return a - 1


def test_basic():
    @validate_inputs(a=int)
    def wrapper(a):
        return f(a)

    assert wrapper(1) == 0
    assert wrapper(9) == 8

    msg = "Incorrect type for variable"
    assert_raises(TypeError, msg, wrapper, 1.5)
    assert_raises(TypeError, msg, wrapper, "foo")

    # We expect Python to handle incorrect
    # argument counts for us before validation.
    py3 = sys.version_info >= (3, 0)

    msg = ("takes 1 positional argument" if py3
           else "takes exactly 1 argument")

    assert_raises(TypeError, msg, wrapper, 1, 1.5)

    msg = ("missing 1 required positional argument" if py3
           else "takes exactly 1 argument")

    assert_raises(TypeError, msg, wrapper)


def test_no_match():
    @validate_inputs(b=int)
    def wrapper(a):
        return f(a)

    assert wrapper(1) == 0
    assert wrapper(1.5) == 0.5

    # No argument matches, so raise whatever
    # error Python is raising natively.
    msg = "unsupported operand type"
    assert_raises(TypeError, msg, wrapper, "foo")


def test_invalid():
    @validate_inputs(a=2)
    def wrapper(a):
        return f(a)

    msg = "Validator must either be a shortcut, callable, or type"
    assert_raises(TypeError, msg, wrapper, 1)


def test_callable():
    @validate_inputs(a=lambda x: x == 1)
    def wrapper(a):
        return f(a)

    assert wrapper(1) == 0

    msg = "Invalid value for variable"
    assert_raises(ValueError, msg, wrapper, 1.5)
    assert_raises(ValueError, msg, wrapper, "foo")


def test_varargs():
    @validate_inputs(a=int)
    def wrapper(a, *_):
        return f(a)

    assert wrapper(1) == 0
    assert wrapper(1, 5) == 0

    msg = "Incorrect type for variable"
    assert_raises(TypeError, msg, wrapper, 1.5, "foo")
    assert_raises(TypeError, msg, wrapper, "foo", "bar")


def test_kwargs():
    @validate_inputs(a=int)
    def wrapper(a, **_):
        return f(a)

    assert wrapper(1) == 0
    assert wrapper(1, b=5, c=2) == 0

    # We expect Python to handle duplicate
    # keyword arguments for us before validation.
    msg = "got multiple values for argument"
    assert_raises(TypeError, msg, wrapper, 1, a=1)


def test_multi_args():
    @validate_inputs(a=int, b=lambda x: x == 1)
    def wrapper(a, b):
        return a + b

    assert wrapper(2, 1) == 3

    msg = "Incorrect type for variable"
    assert_raises(TypeError, msg, wrapper, a="foo", b=1)

    msg = "Invalid value for variable"
    assert_raises(ValueError, msg, wrapper, a=1, b=2)


class TestShortcuts(object):

    def test_number(self):
        @validate_inputs(a="number")
        def wrapper(a):
            return f(a)

        assert wrapper(1) == 0

        msg = "Expected a number but got"
        assert_raises(TypeError, msg, wrapper, "foo")

    def test_integer(self):
        @validate_inputs(a="integer")
        def wrapper(a):
            return f(a)

        assert wrapper(1) == 0

        msg = "Expected an integer but got"
        assert_raises(TypeError, msg, wrapper, "foo")
        assert_raises(TypeError, msg, wrapper, 1.0)

    def test_even(self):
        @validate_inputs(a="even")
        def wrapper(a):
            return f(a)

        assert wrapper(2) == 1

        msg = "Expected an integer but got"
        assert_raises(TypeError, msg, wrapper, "foo")
        assert_raises(TypeError, msg, wrapper, 2.0)

        msg = "Expected an even integer"
        assert_raises(ValueError, msg, wrapper, 1)
        assert_raises(ValueError, msg, wrapper, 3)

    def test_odd(self):
        @validate_inputs(a="odd")
        def wrapper(a):
            return f(a)

        assert wrapper(1) == 0

        msg = "Expected an integer but got"
        assert_raises(TypeError, msg, wrapper, "foo")
        assert_raises(TypeError, msg, wrapper, 1.0)

        msg = "Expected an odd integer"
        assert_raises(ValueError, msg, wrapper, 2)
        assert_raises(ValueError, msg, wrapper, 4)
