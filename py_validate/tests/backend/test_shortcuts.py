import py_validate.backend.shortcuts as shortcuts

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

        with pytest.raises(TypeError) as exc_info:
            shortcuts.check_number(invalid)

        exc_info.match(msg)

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

        with pytest.raises(TypeError) as exc_info:
            shortcuts.check_integer(invalid)

        exc_info.match(msg)

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

            with pytest.raises(TypeError) as exc_info:
                shortcuts.check_integer(dtype(1))

            exc_info.match(msg)
