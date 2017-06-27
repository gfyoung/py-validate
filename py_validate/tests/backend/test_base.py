"""
Unittests for fuzzy inputs to the `ValidatedFunction` class as well as
the namespace members with imports from top and lower-level modules.
"""

from py_validate.backend import ValidatedFunction
from py_validate.tests import assert_raises

import pytest


class TestNamespace(object):

    @staticmethod
    def _check_namespace(namespace, expected):
        """
        Check that the module namespace matches what we expect it to contain.

        Parameters
        ----------
        namespace : module
            The module that we are to check.
        expected : set
            Set of method and object names that we expect it to contain, no
            more, no less (excluding attributes starting with "__")

        Raises
        ------
        AssertionError : the check failed.
        """

        namespace = set([f for f in dir(namespace) if not f.startswith("__")])
        assert len(namespace ^ expected) == 0

    def test_pv_namespace(self):
        import py_validate as pv
        expected = {"backend", "test", "validate_inputs",
                    "tests", "validate_outputs", "validator"}

        self._check_namespace(pv, expected)

    def test_pv_backend_namespace(self):
        import py_validate.backend as backend
        expected = {"NegateShortcut", "ValidatedFunction", "base",
                    "get_shortcut", "helpers", "shortcuts"}

        self._check_namespace(backend, expected)


class TestValidatedFunction(object):

    @pytest.mark.parametrize("invalid", [
        2, [1, 2, 3], {1: 2, 4: 5}
    ])
    def test_input_not_callable(self, invalid):
        msg = "Invalid function parameter provided"
        assert_raises(ValueError, msg, ValidatedFunction, invalid)

    class CallableClassNoCode(object):
        def __call__(self):
            pass

    class CallableClassNoCoVarnames(object):
        def __call__(self):
            pass

        @property
        def __code__(self):
            return "foo"

    @pytest.mark.parametrize("klass", [
        CallableClassNoCode, CallableClassNoCoVarnames
    ])
    def test_input_wrong_callable(self, klass):
        msg = "Invalid function parameter provided"
        assert_raises(ValueError, msg, ValidatedFunction, klass())

    def test_input_duplicate_variable(self):
        validator = ValidatedFunction(lambda x: x + 1)
        validator.update_input_validators(x=int)

        msg = "Validator\(s\) for input"
        assert_raises(ValueError, msg,
                      validator.update_input_validators, x=float)

    def test_input_bad_exp_len(self):
        validator = ValidatedFunction(lambda x: x + 1)
        msg = "Expected an integer for expected output length"
        assert_raises(TypeError, msg, validator.update_exp_output_len, 1.0)
        assert_raises(TypeError, msg, validator.update_exp_output_len, "foo")

        validator = ValidatedFunction(lambda x: x + 1)
        msg = "Expected output length must be positive or -1"
        assert_raises(ValueError, msg, validator.update_exp_output_len, -2)
