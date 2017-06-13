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

        for dtype in np.typecodes["AllInteger"]:
            dtype = np.dtype(dtype).type
            shortcuts.check_number(dtype(1))
