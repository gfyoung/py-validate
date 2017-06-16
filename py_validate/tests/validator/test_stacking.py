"""
Stacking tests for the decorators i.e. how functions behave when
we start applying more than one of these decorators to a function.
"""

from py_validate.validator import validate_inputs, validate_outputs
from py_validate.tests import assert_raises


@validate_inputs(a=int)
@validate_inputs(b=int)
def sum_numbers(a, b):
    return a + b


@validate_inputs(a=float)
@validate_inputs(a=int)
def sum_numbers_input_override(a, b):
    return a + b


@validate_inputs(a=int)
@validate_outputs(None, int)
def sum_numbers_input_output(a, b):
    return a + b


@validate_outputs(None, int)
@validate_inputs(a=int)
def sum_numbers_output_input(a, b):
    return a + b


@validate_outputs(None, int)
@validate_outputs(None, float)
def op_numbers_two_outputs(a, b):
    return a + 1, b - 1


@validate_outputs(3)
@validate_inputs(a=lambda x: x > 0)
@validate_outputs(None, lambda x: x % 3 == 0)
def triple_input_triple_output(a):
    if a % 3 == 0:
        return a, a, a
    elif a % 3 == 1:
        return a, a - 1, a + 1
    else:
        return a


@validate_inputs(a=1)
@validate_outputs(1, int)
def operate_invalid_input_check(a):
    return a - 1


@validate_inputs(a=int)
@validate_outputs(1, 1)
def operate_invalid_output_check(a):
    return a - 1


@validate_inputs(a="odd")
@validate_inputs(b="number")
@validate_outputs(None, "even")
def operate_invalid_numbers(a, b):
    return a + b


@validate_inputs(a="integer")
@validate_outputs(1, int)
def operate_integer_in_out(a):
    if a == 0:
        return 0.5
    elif a == 1:
        return 1, 1
    else:
        return a + 1


def test_valid():
    assert sum_numbers(1, 2) == 3
    assert operate_integer_in_out(2) == 3
    assert operate_invalid_numbers(1, 1) == 2
    assert sum_numbers_input_output(1, 2) == 3
    assert sum_numbers_output_input(1, 2) == 3
    assert sum_numbers_input_override(1.5, 1) == 2.5
    assert op_numbers_two_outputs(1.5, 2) == (2.5, 1)


def test_invalid_type():
    msg = "Validator must either be a shortcut, callable, or type"
    assert_raises(TypeError, msg, operate_invalid_input_check, 1)
    assert_raises(TypeError, msg, operate_invalid_output_check, 1)

    msg = "Incorrect type for variable"
    assert_raises(TypeError, msg, sum_numbers, 1.5, 1)
    assert_raises(TypeError, msg, sum_numbers, 1, 1.5)
    assert_raises(TypeError, msg, sum_numbers, 1.5, 2.5)
    assert_raises(TypeError, msg, sum_numbers_input_output, 1.5, 1.5)
    assert_raises(TypeError, msg, sum_numbers_output_input, 1.5, 1.5)

    # Float is now the expected type for
    # the first argument to the function.
    assert_raises(TypeError, msg, sum_numbers_input_override, 1, 2)

    # Output type check should fail.
    assert_raises(TypeError, msg, sum_numbers_input_output, 1, 1.5)
    assert_raises(TypeError, msg, sum_numbers_output_input, 1, 1.5)

    assert_raises(TypeError, msg, operate_integer_in_out, 0)
    assert_raises(TypeError, msg, op_numbers_two_outputs, 1, 2)
    assert_raises(TypeError, msg, op_numbers_two_outputs, 1, 1.5)

    msg = "Expected a number but got"
    assert_raises(TypeError, msg, operate_invalid_numbers, 1, "foo")

    msg = "Expected an integer but got"
    assert_raises(TypeError, msg, operate_invalid_numbers, "foo", 1)
    assert_raises(TypeError, msg, operate_invalid_numbers, "foo", "bar")

    msg = "Expected an integer but got"
    assert_raises(TypeError, msg, operate_integer_in_out, 1.5)

    msg = "Expected an even integer"
    assert_raises(ValueError, msg, operate_invalid_numbers, 1, 2)


def test_failed_validator():
    msg = "Invalid value for variable"
    assert_raises(ValueError, msg, triple_input_triple_output, 1)
    assert_raises(ValueError, msg, triple_input_triple_output, -1)


def test_failed_output_len():
    msg = "items returned but got"
    assert_raises(ValueError, msg, operate_integer_in_out, 1)
    assert_raises(ValueError, msg, triple_input_triple_output, 5)
