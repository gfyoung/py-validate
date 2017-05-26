"""
Integration tests for the decorators.
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
@validate_outputs(int)
def sum_numbers_input_output(a, b):
    return a + b


@validate_outputs(int)
@validate_inputs(a=int)
def sum_numbers_output_input(a, b):
    return a + b


@validate_outputs(int)
@validate_outputs(float)
def op_numbers_two_outputs(a, b):
    return a + 1, b - 1


def test_valid():
    assert sum_numbers(1, 2) == 3
    assert sum_numbers_input_output(1, 2) == 3
    assert sum_numbers_output_input(1, 2) == 3
    assert sum_numbers_input_override(1.5, 1) == 2.5
    assert op_numbers_two_outputs(1.5, 2) == (2.5, 1)


def test_invalid_type():
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
