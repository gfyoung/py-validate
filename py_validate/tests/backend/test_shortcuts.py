import py_validate.backend.shortcuts as shortcuts
from py_validate.tests import assert_raises

import pytest


class TestCheckNumber(object):

    @pytest.mark.parametrize("valid", [
        2, -1, 1.5, -3, 4.5, 99, -36.4
    ])
    def test_valid_number(self, valid):
        shortcuts.check_number(valid)

    @pytest.mark.parametrize("invalid", [
        [1, 2], "foo", (1, 2), Exception(""), False
    ])
    def test_invalid_number(self, invalid):
        msg = "Expected a number but got"
        assert_raises(TypeError, msg, shortcuts.check_number, invalid)

    def test_numpy_dtypes(self):
        np = pytest.importorskip("numpy")
        dtypes = (np.typecodes["AllInteger"] +
                  np.typecodes["AllFloat"] +
                  np.typecodes["Complex"])

        for dtype in dtypes:
            dtype = np.dtype(dtype).type
            shortcuts.check_number(dtype(1))


class TestCheckInteger(object):

    @pytest.mark.parametrize("valid", [
        2, -1, 1, -3, 5, 99, -36
    ])
    def test_valid_integer(self, valid):
        shortcuts.check_integer(valid)

    @pytest.mark.parametrize("invalid", [
        1.5, -1.0, [1, 2], "foo", (1, 2), True
    ])
    def test_invalid_integer(self, invalid):
        msg = "Expected an integer but got"
        assert_raises(TypeError, msg, shortcuts.check_integer, invalid)

    def test_numpy_dtypes(self):
        np = pytest.importorskip("numpy")
        dtypes = np.typecodes["AllInteger"]

        for dtype in dtypes:
            dtype = np.dtype(dtype).type
            shortcuts.check_integer(dtype(1))

        # The integer check is strict. The
        # type must match, even if numerically
        # the number is an integer.
        msg = "Expected an integer but got"
        dtypes = (np.typecodes["AllFloat"] +
                  np.typecodes["Complex"])

        for dtype in dtypes:
            dtype = np.dtype(dtype).type
            assert_raises(TypeError, msg, shortcuts.check_integer, dtype(1))


class TestCheckEven(object):

    @pytest.mark.parametrize("valid", [
        2, 4, 6, -10, 14, 100
    ])
    def test_valid_even(self, valid):
        shortcuts.check_even(valid)

    @pytest.mark.parametrize("invalid", [
        1.5, -2.0, [1, 2], "foo", (1, 2), True
    ])
    def test_invalid_even_not_int(self, invalid):
        msg = "Expected an integer but got"
        assert_raises(TypeError, msg, shortcuts.check_even, invalid)

    @pytest.mark.parametrize("invalid", [
        1, -1, 3, 11, 101, 7, 3
    ])
    def test_invalid_even_not_even(self, invalid):
        msg = "Expected an even integer"
        assert_raises(ValueError, msg, shortcuts.check_even, invalid)


class TestCheckOdd(object):

    @pytest.mark.parametrize("valid", [
        1, -1, 3, 11, 101, 7, 3
    ])
    def test_valid_odd(self, valid):
        shortcuts.check_odd(valid)

    @pytest.mark.parametrize("invalid", [
        1.5, -2.0, [1, 2], "foo", (1, 2), True
    ])
    def test_invalid_odd_not_int(self, invalid):
        msg = "Expected an integer but got"
        assert_raises(TypeError, msg, shortcuts.check_odd, invalid)

    @pytest.mark.parametrize("invalid", [
        2, 4, 6, -10, 14, 100
    ])
    def test_invalid_even_not_even(self, invalid):
        msg = "Expected an odd integer"
        assert_raises(ValueError, msg, shortcuts.check_odd, invalid)
