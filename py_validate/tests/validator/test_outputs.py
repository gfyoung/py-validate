"""
Unittests for the output validator decorator.
"""

from py_validate.backend.shortcuts import NegateFailure
from py_validate.validator import validate_outputs
from py_validate.tests import assert_raises


def f(a):
    return a


class TestOutputCount(object):

    def test_output_no_count(self):
        @validate_outputs(None)
        def wrapper(a):
            if a == 1:
                return f(a), f(a)
            else:
                return f(a)

        # No output count, no check.
        assert wrapper(2) == 2
        assert wrapper(1) == (1, 1)

    def test_output_positive_count(self):
        @validate_outputs(2)
        def wrapper(a):
            if a == 1:
                return f(a), f(a)
            else:
                return f(a)

        assert wrapper(1) == (1, 1)

        msg = "items returned but got"
        assert_raises(ValueError, msg, wrapper, 2)

    def test_output_negative_count_no_validators(self):
        @validate_outputs(-1)
        def wrapper(a):
            if a == 1:
                return f(a), f(a)
            else:
                return f(a)

        # Tuples are validated as is, and since
        # no validators are provided, all outputs
        # are accepted in this case.
        assert wrapper(0) == 0
        assert wrapper(1) == (1, 1)

    def test_output_negative_count_validators(self):
        @validate_outputs(-1, tuple)
        def wrapper(a):
            if a == 1:
                return f(a), f(a)
            else:
                return f(a)

        # Tuples are validated as is, and in this
        # case, we specifically check that we get
        # a tuple from the function.
        assert wrapper(1) == (1, 1)

        msg = "Incorrect type for variable"
        assert_raises(TypeError, msg, wrapper, 0)


def test_basic():
    @validate_outputs(None, int)
    def wrapper(a):
        return f(a)

    assert wrapper(1) == 1
    assert wrapper(9) == 9

    msg = "Incorrect type for variable"
    assert_raises(TypeError, msg, wrapper, 1.5)
    assert_raises(TypeError, msg, wrapper, "foo")
    assert_raises(TypeError, msg, wrapper, [1, 2, 3])


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
        assert_raises(TypeError, msg, wrapper, {1, 2})

    def test_integer(self):
        @validate_outputs(None, "integer")
        def wrapper(a):
            return f(a)

        assert wrapper(1) == 1

        msg = "Expected an integer"
        assert_raises(TypeError, msg, wrapper, 1.5)
        assert_raises(TypeError, msg, wrapper, "foo")
        assert_raises(TypeError, msg, wrapper, [-1, -3])

    def test_even(self):
        @validate_outputs(None, "even")
        def wrapper(a):
            return f(a)

        assert wrapper(2) == 2

        msg = "Expected an integer"
        assert_raises(TypeError, msg, wrapper, 1.5)
        assert_raises(TypeError, msg, wrapper, "foo")
        assert_raises(TypeError, msg, wrapper, [3, 4])

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
        assert_raises(TypeError, msg, wrapper, dict())

        msg = "Expected an odd integer"
        assert_raises(ValueError, msg, wrapper, 2)

    def test_negate(self):
        @validate_outputs(-1, "~integer")
        def wrapper(a):
            return a

        assert wrapper(1.5) == 1.5
        assert wrapper("foo") == "foo"
        assert wrapper((1, 2, 3)) == (1, 2, 3)

        msg = "'integer' passed when it shouldn't have"
        assert_raises(NegateFailure, msg, wrapper, 1)
