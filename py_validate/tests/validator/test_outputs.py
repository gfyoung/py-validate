"""
Unittests for the output validator decorator.
"""

from py_validate.validator import validate_outputs
from py_validate.tests import assert_raises


def f(a):
    return a


def test_output_no_count():
    @validate_outputs(None)
    def wrapper(a):
        if a == 1:
            return f(a), f(a)
        else:
            return f(a)

    # No output count, no check.
    assert wrapper(2) == 2
    assert wrapper(1) == (1, 1)


def test_output_count():
    @validate_outputs(2)
    def wrapper(a):
        if a == 1:
            return f(a), f(a)
        else:
            return f(a)

    assert wrapper(1) == (1, 1)

    msg = "items returned but got"
    assert_raises(ValueError, msg, wrapper, 2)


def test_basic():
    @validate_outputs(None, int)
    def wrapper(a):
        return f(a)

    assert wrapper(1) == 1
    assert wrapper(9) == 9

    msg = "Incorrect type for variable"
    assert_raises(TypeError, msg, wrapper, 1.5)
    assert_raises(TypeError, msg, wrapper, 1.0)


def test_no_match():
    @validate_outputs(None, None, int)
    def wrapper(a):
        return f(a)

    assert wrapper(1) == 1
    assert wrapper(2.0) == 2


def test_callable():
    @validate_outputs(None, lambda x: x == 1)
    def wrapper(a):
        return f(a)

    assert wrapper(1) == 1

    msg = "Invalid value for variable"
    assert_raises(ValueError, msg, wrapper, 1.5)


def test_multi_args():
    @validate_outputs(2, lambda x: x == 1, int)
    def wrapper(a):
        if a in (0, 1):
            return a, f(a)
        elif a == 2:
            return 1, 1.5
        else:
            return a

    assert wrapper(1) == (1, 1)

    msg = "Invalid value for variable"
    assert_raises(ValueError, msg, wrapper, 0)

    msg = "Incorrect type for variable"
    assert_raises(TypeError, msg, wrapper, 2)

    msg = "items returned but got"
    assert_raises(ValueError, msg, wrapper, 3)


class TestShortcuts(object):

    def test_number(self):
        @validate_outputs(None, "number")
        def wrapper(a):
            return f(a)

        assert wrapper(1) == 1
        assert wrapper(1.5) == 1.5

        msg = "Expected a number but got"
        assert_raises(TypeError, msg, wrapper, "foo")

    def test_integer(self):
        @validate_outputs(None, "integer")
        def wrapper(a):
            return f(a)

        assert wrapper(1) == 1

        msg = "Expected an integer"
        assert_raises(TypeError, msg, wrapper, 1.5)
        assert_raises(TypeError, msg, wrapper, "foo")

    def test_even(self):
        @validate_outputs(None, "even")
        def wrapper(a):
            return f(a)

        assert wrapper(2) == 2

        msg = "Expected an integer"
        assert_raises(TypeError, msg, wrapper, 1.5)
        assert_raises(TypeError, msg, wrapper, "foo")

        msg = "Expected an even integer"
        assert_raises(ValueError, msg, wrapper, 1)

    def test_odd(self):
        @validate_outputs(None, "odd")
        def wrapper(a):
            return f(a)

        assert wrapper(1) == 1

        msg = "Expected an integer"
        assert_raises(TypeError, msg, wrapper, 1.5)
        assert_raises(TypeError, msg, wrapper, "foo")

        msg = "Expected an odd integer"
        assert_raises(ValueError, msg, wrapper, 2)
