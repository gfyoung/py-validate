"""
Unittests for the helper functions and objects.
"""

from py_validate.backend.base import DocSubstitution, FrozenDict
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
