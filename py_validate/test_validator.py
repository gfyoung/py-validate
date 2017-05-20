import pytest

from py_validate.validator import validate_inputs


@validate_inputs(a=int)
def increment(a):
    return a + 1


@validate_inputs(a=int)
def increment_no_match(b):
    return b - 1


@validate_inputs(a=lambda x: x % 2 == 0)
def operate_only_even(a):
    return (a / 2) - 5


@validate_inputs(a=int)
def validate_odd(a):
    if a % 2 != 1:
        raise ValueError("Odd number expected")


@validate_inputs(a=validate_odd)
def operate_only_odd(a):
    return ((a - 1) / 2) - 5


def test_valid():
    assert increment(1) == 2
    assert increment_no_match(5) == 4

    assert operate_only_odd(7) == -2
    assert operate_only_even(2) == -4


def test_wrong_number_of_args():
    # We expect Python to handle this for us.

    with pytest.raises(TypeError) as exc_info:
        increment(1, 1.5)

    exc_info.match("takes 1 positional argument")

    with pytest.raises(TypeError) as exc_info:
        increment()

    exc_info.match("missing 1 required positional argument")


def test_invalid_type():
    with pytest.raises(TypeError) as exc_info:
        increment(1.5)

    exc_info.match("Incorrect type passed in")

    with pytest.raises(TypeError) as exc_info:
        operate_only_odd(1.5)

    exc_info.match("Incorrect type passed in")

    # No argument matches, so raise whatever
    # error Python is raising natively.
    with pytest.raises(TypeError) as exc_info:
        increment_no_match("foo")

    exc_info.match("unsupported operand type")


def test_failed_validator():
    with pytest.raises(ValueError) as exc_info:
        operate_only_even(3)

    exc_info.match("Invalid argument value")

    # The validation function itself will fail
    # because the argument has no mod method.
    with pytest.raises(TypeError) as exc_info:
        operate_only_even(tuple())

    exc_info.match("unsupported operand type")

    with pytest.raises(ValueError) as exc_info:
        operate_only_odd(2)

    exc_info.match("Odd number expected")
