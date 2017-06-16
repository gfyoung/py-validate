"""
Unittests for the output validator decorator.
"""

from py_validate.validator import validate_outputs
from py_validate.tests import assert_raises


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


@validate_outputs(None, "number")
def operate_invalid_number(a):
    return a * 5


@validate_outputs(2, "integer")
def operate_invalid_integer(a):
    if a % 2 == 0:
        return 1 if a == 2 else (a, a)
    else:
        return float(a), float(a)


@validate_outputs(None, "even")
def operate_double_except_one(a):
    if a == 1:
        return a
    else:
        return 2 * int(a)


@validate_outputs(None, "odd")
def operate_odd_except_one(a):
    if a == 1:
        return a + 1
    else:
        return 2 * int(a) + 1


def test_valid():
    # The types are correct.
    assert halve_input(2) == 1
    assert operate_invalid_number(5) == 25
    assert operate_invalid_integer(4) == (4, 4)

    # These should pass validation.
    assert operate_odd_except_one(2) == 5
    assert operate_double_except_one(2) == 4
    assert triple_quadruple_input(2) == (6, 8)

    # Correct count and pass validation
    assert triple_input_triple_output(3) == (3, 3, 3)


def test_invalid_type():
    msg = "Validator must either be a shortcut, callable, or type"
    assert_raises(TypeError, msg, operate_invalid_check, 1)

    msg = "Incorrect type for variable"
    assert_raises(TypeError, msg, halve_input, 1)

    msg = "Expected a number but got"
    assert_raises(TypeError, msg, operate_invalid_number, "a")

    msg = "Expected an integer but got"
    assert_raises(TypeError, msg, operate_invalid_integer, 1)

    msg = "Expected an even integer"
    assert_raises(ValueError, msg, operate_double_except_one, 1)

    msg = "Expected an odd integer"
    assert_raises(ValueError, msg, operate_odd_except_one, 1)


def test_failed_validator():
    msg = "Invalid value for variable"
    assert_raises(ValueError, msg, triple_quadruple_input, 1)
    assert_raises(ValueError, msg, triple_input_triple_output, 4)


def test_failed_output_len():
    msg = "items returned but got"
    assert_raises(ValueError, msg, operate_invalid_integer, 2)
    assert_raises(ValueError, msg, triple_input_triple_output, 5)
