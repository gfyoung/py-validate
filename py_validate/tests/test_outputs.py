"""
Unittests for the output validator decorator.
"""

from py_validate.validator import validate_outputs

import pytest


@validate_outputs(None, int)
def halve_input(a):
    if a % 2 == 0:
        return a // 2
    else:
        return float(a)


def validate_multiple_three(a):
    return a % 3 == 0


def validate_multiple_four(a):
    return a % 4 == 0


@validate_outputs(None, validate_multiple_three,
                  validate_multiple_four)
def triple_quadruple_input(a):
    if a % 2 == 0:
        return 3 * a, 4 * a
    else:
        return 1, 2


@validate_outputs(3, validate_multiple_three)
def triple_input_triple_output(a):
    if a % 3 == 0:
        return a, a, a
    elif a % 3 == 1:
        return a, a - 1, a + 1
    else:
        return a


@validate_outputs(None, 2)
def operate_invalid_check(a):
    return a + 1


def test_valid():
    # The types are correct.
    assert halve_input(2) == 1

    # These should pass validation.
    assert triple_quadruple_input(2) == (6, 8)

    # Correct count and pass validation
    assert triple_input_triple_output(3) == (3, 3, 3)


def test_invalid_type():
    matcher = "Validator must either be a callable or type"

    with pytest.raises(TypeError) as exc_info:
        operate_invalid_check(1)

    exc_info.match(matcher)

    matcher = "Incorrect type for variable"

    with pytest.raises(TypeError) as exc_info:
        halve_input(1)

    exc_info.match(matcher)


def test_failed_validator():
    matcher = "Invalid value for variable"

    with pytest.raises(ValueError) as exc_info:
        triple_quadruple_input(1)

    exc_info.match(matcher)

    with pytest.raises(ValueError) as exc_info:
        triple_input_triple_output(4)

    exc_info.match(matcher)


def test_failed_output_len():
    matcher = "items returned but got"

    with pytest.raises(ValueError) as exc_info:
        triple_input_triple_output(5)

    exc_info.match(matcher)
