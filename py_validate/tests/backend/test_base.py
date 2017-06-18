"""
Unittests for fuzzy inputs to the `_ValidatedFunction` class.
"""

from py_validate.backend.base import DocSubstitution, FrozenDict
from py_validate.backend import ValidatedFunction
from py_validate.tests import assert_raises

import pytest


class TestFrozenDict(object):

    def test_init(self):
        d = FrozenDict()
        assert len(d) == 0

        d = FrozenDict(a=1)
        assert len(d) == 1
        assert d["a"] == 1

        d = FrozenDict({"a": 1})
        assert len(d) == 1
        assert d["a"] == 1

        d = FrozenDict([("a", 1), ("b", 2)])
        assert len(d) == 2
        assert d["a"] == 1
        assert d["b"] == 2

    def test_set_item(self):
        d = FrozenDict()

        d[1] = 2
        assert d[1] == 2
        assert len(d) == 1

        d[2] = 3
        assert d[2] == 3
        assert len(d) == 2

        assert_raises(KeyError, None, d.__setitem__, 1, 3)

    def test_del_item(self):
        d = FrozenDict({1: 2})

        del d[1]
        assert len(d) == 0

        assert_raises(KeyError, None, d.__delitem__, 1)

    def test_reset_key(self):
        d = FrozenDict()

        d[1] = 2
        del d[1]

        # Can set key "1" again.
        d[1] = 3
        assert d[1] == 3
        assert len(d) == 1

    def test_update(self):
        d = FrozenDict()

        d.update({1: 2})
        assert d[1] == 2
        assert len(d) == 1

        d.update([(3, 4)])
        assert d[3] == 4
        assert len(d) == 2

        d.update(foo=2)
        assert d["foo"] == 2
        assert len(d) == 3

        assert_raises(KeyError, None, d.update, foo=3)
        assert_raises(KeyError, None, d.update, {3: 5})
        assert_raises(KeyError, None, d.update, [(1, 3)])


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
        expected = {"ValidatedFunction", "base",
                    "get_shortcut", "shortcuts"}

        self._check_namespace(backend, expected)


class TestDocSubstitution(object):

    @pytest.mark.parametrize("tabs", [0, 1, 2])
    def test_doc_no_substitute(self, tabs):
        doc_substitution = DocSubstitution(tabs=tabs, name="foo")

        @doc_substitution
        def f():
            """
            Returns 1.
            """
            return 1

        # Tab count doesn't matter since there is no substitution.
        assert f.__doc__ == "\n            Returns 1.\n            "

    @pytest.mark.parametrize("tabs", [0, 1, 2])
    def test_doc_substitute_single(self, tabs):
        doc_substitution = DocSubstitution(tabs=tabs, name="foo")

        @doc_substitution
        def f():
            """
            Returns {name}.
            """
            return "foo"

        # Tab count doesn't matter since there is no multi-line substitution.
        assert f.__doc__ == "\n            Returns foo.\n            "

    @pytest.mark.parametrize("tabs", [0, 1, 2])
    def test_doc_substitute_multi(self, tabs):
        doc_substitution = DocSubstitution(tabs=tabs, name="foo\nbar")

        @doc_substitution
        def f():
            """
            Returns {name}.
            """
            return "foo\nbar"

        # Now the tab count matters because the substitution is multi-line.
        assert f.__doc__ == ("\n            Returns foo\n" +
                             "    " * tabs + "bar.\n            ")

    @pytest.mark.parametrize("tabs", [0, 1, 2])
    def test_doc_substitute_multi_override(self, tabs):
        override_tab_count = 3
        doc_substitution = DocSubstitution(tabs=tabs,
                                           name=("foo\nbar",
                                                 override_tab_count))

        @doc_substitution
        def f():
            """
            Returns {name}.
            """
            return "foo\nbar"

        # Now the tab count matters because the substitution is multi-line.
        assert f.__doc__ == ("\n            Returns foo\n" +
                             "    " * override_tab_count + "bar.\n" +
                             "            ")

    @pytest.mark.parametrize("tabs", [0, 1, 2])
    def test_doc_multi_substitute(self, tabs):
        doc_substitution = DocSubstitution(tabs=tabs, name="foo\nbar",
                                           explanation="We do this because "
                                                       "it is necessary.")

        @doc_substitution
        def f():
            """
            Returns {name}.

            {explanation}
            """
            return "foo"

        # The tab count matters because one of the substitutions is multi-line.
        assert f.__doc__ == ("\n            Returns foo\n" +
                             "    " * tabs + "bar.\n\n" +
                             "            We do this because it is necessary."
                             "\n            ")

    @pytest.mark.parametrize("tabs", [0, 1, 2])
    def test_doc_multi_substitute_override(self, tabs):
        override_tab_count = 3
        doc_substitution = DocSubstitution(tabs=tabs, name="foo\nbar",
                                           explanation=("We do this because\n"
                                                        "it is necessary.",
                                                        override_tab_count))

        @doc_substitution
        def f():
            """
            Returns {name}.

            {explanation}
            """
            return "foo"

        # The tab count matters because one of the substitutions is multi-line.
        assert f.__doc__ == ("\n            Returns foo\n" +
                             "    " * tabs + "bar.\n\n" +
                             "            We do this because\n" +
                             "    " * override_tab_count + "it is necessary.\n"
                             "            ")


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
