from py_validate.validator import validate_outputs

import pytest


@validate_outputs(int)
def halve_input(a):
    if a % 2 == 0:
        return a // 2
    else:
        return float(a)


def validate_multiple_three(a):
    return a % 3 == 0


def validate_multiple_four(a):
    return a % 4 == 0


@validate_outputs(validate_multiple_three,
                  validate_multiple_four)
def triple_quadruple_input(a):
    if a % 2 == 0:
        return 3 * a, 4 * a
    else:
        return 1, 2


def test_valid():
    # The types are correct.
    assert halve_input(2) == 1

    # These should pass validation.
    assert triple_quadruple_input(2) == (6, 8)


def test_invalid_type():
    with pytest.raises(TypeError) as exc_info:
        halve_input(1)

    exc_info.match("Incorrect type for variable")


def test_failed_validator():
    with pytest.raises(ValueError) as exc_info:
        triple_quadruple_input(1)

    exc_info.match("Invalid value for variable")
