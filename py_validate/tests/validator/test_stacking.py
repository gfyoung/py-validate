"""
Stacking tests for the decorators i.e. how functions behave when start
applying more than one of these decorators to a function.
"""

from py_validate.validator import validate_inputs, validate_outputs

import pytest


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


def test_valid():
    assert sum_numbers(1, 2) == 3
    assert sum_numbers_input_output(1, 2) == 3
    assert sum_numbers_output_input(1, 2) == 3
    assert sum_numbers_input_override(1.5, 1) == 2.5
    assert op_numbers_two_outputs(1.5, 2) == (2.5, 1)


def test_invalid_type():
    matcher = "Validator must either be a callable or type"

    with pytest.raises(TypeError) as exc_info:
        operate_invalid_input_check(1)

    exc_info.match(matcher)

    with pytest.raises(TypeError) as exc_info:
        operate_invalid_output_check(1)

    exc_info.match(matcher)

    matcher = "Incorrect type for variable"

    with pytest.raises(TypeError) as exc_info:
        sum_numbers(1.5, 1)

    exc_info.match(matcher)

    with pytest.raises(TypeError) as exc_info:
        sum_numbers(1, 1.5)

    exc_info.match(matcher)

    with pytest.raises(TypeError) as exc_info:
        sum_numbers(1.5, 2.5)

    exc_info.match(matcher)

    with pytest.raises(TypeError) as exc_info:
        sum_numbers_input_output(1.5, 1.5)

    exc_info.match(matcher)

    with pytest.raises(TypeError) as exc_info:
        sum_numbers_output_input(1.5, 1.5)

    exc_info.match(matcher)

    # Float is now the expected type for
    # the first argument to the function.
    with pytest.raises(TypeError) as exc_info:
        sum_numbers_input_override(1, 2)

    exc_info.match(matcher)

    # Output type check should fail.
    with pytest.raises(TypeError) as exc_info:
        sum_numbers_input_output(1, 1.5)

    exc_info.match(matcher)

    with pytest.raises(TypeError) as exc_info:
        sum_numbers_output_input(1, 1.5)

    exc_info.match(matcher)

    with pytest.raises(TypeError) as exc_info:
        op_numbers_two_outputs(1, 2)

    exc_info.match(matcher)

    with pytest.raises(TypeError) as exc_info:
        op_numbers_two_outputs(1, 1.5)

    exc_info.match(matcher)


def test_failed_validator():
    matcher = "Invalid value for variable"

    with pytest.raises(ValueError) as exc_info:
        triple_input_triple_output(1)

    exc_info.match(matcher)

    with pytest.raises(ValueError) as exc_info:
        triple_input_triple_output(-1)

    exc_info.match(matcher)


def test_failed_output_len():
    matcher = "items returned but got"

    with pytest.raises(ValueError) as exc_info:
        triple_input_triple_output(5)

    exc_info.match(matcher)
