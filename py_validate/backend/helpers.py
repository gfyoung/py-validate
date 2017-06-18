"""
Helper classes and objects that facilitate functionality in other modules.
"""


class DocSubstitution(object):
    """
    Decorator class for substituting variables in docstring templates.

    This is an internal class, so we will not be verifying parameters
    in any way in this function. We trust the developer will not pass
    in incorrect inputs to this class.
    """

    def __init__(self, tabs=0, **kwargs):
        """
        Initialize a DocSubstitution instance.

        Parameters
        ----------
        tabs : int, default 0
            The number of "tabs" (or rather, four spaces) we use
            to indent each line of the substituted value. This will
            impact how they are displayed in the docstring.

            This is also the default tabbing in case we pass in special
            tabbing requirements for a specific docstring substitution.
        kwargs : kwargs
            The parameters that we are going to pass into the function
            docstring so that it displays the correct documentation.

            The value of each key can either be the docstring that
            we are expecting or a tuple of length two comprised of
            the docstring and the tabbing for that docstring.
        """

        formatted_kwargs = {}

        for param, value in kwargs.items():
            if isinstance(value, tuple):
                value, tabs_count = value
            else:  # just the parameter value
                tabs_count = tabs

            new_lines = [line for line in value.split("\n")]
            new_value = ("\n" + "    " * tabs_count).join(new_lines)

            formatted_kwargs[param] = new_value

        self.params = formatted_kwargs

    def __call__(self, f):
        """
        Wrapper method around calling `f`.

        Before calling the function, the docstring is filled with the
        parameters specified in the constructor (`self.params`).

        Returns
        -------
        new_f : callable
            The same method `f` with the filled-in documentation.
        """

        f.__doc__ = f.__doc__ and f.__doc__.format(**self.params)
        return f


class FrozenDict(dict):
    """
    Dictionary in which keys, once set, cannot be updated unless the
    key is deleted and set once again.

    This is an internal class, so we will not be verifying parameters
    in any way in this function. We trust the developer will not pass
    in incorrect inputs to this class.
    """

    def __setitem__(self, key, value):
        """
        Override `dict.__setitem__` by checking whether the key exists
        in the dictionary before setting the key.

        Parameters
        ----------
        key : object
            The key to hash and set in the dictionary.
        value : object
            The associated value to the key in the dictionary.

        Raises
        ------
        KeyError : the key already exists in the dictionary.
        """

        if key in self:
            raise KeyError(key)

        dict.__setitem__(self, key, value)

    def update(self, new_mappings=None, **keyword_mappings):
        """
        Override `dict.update` by explicitly calling our own
        `self.__setitem__` method to disallow resetting a key.

        Parameters
        ----------
        new_mappings : object, default None
            An object used to update the dictionary, but the method
            by which we do it depends on two cases:

            1) `new_mappings` has a `.keys()` method

                for k in new_mappings:
                    self[k] = new_mappings[k]

            2) `new_mappings` has no `.keys()` method

                for k, v in new_mappings:
                    self[k] = v

        keyword_mappings : kwargs
            Additional object used to update the dictionary with
            keyword arguments.

        Raises
        ------
        KeyError : one of keys already exists in the dictionary.
        """

        if new_mappings is not None:
            keys_method = getattr(new_mappings, "keys", None)
            if callable(keys_method):
                for k in new_mappings:
                    self.__setitem__(k, new_mappings[k])
            else:
                for k, v in new_mappings:
                    self.__setitem__(k, v)

        for k, v in keyword_mappings.items():
            self.__setitem__(k, v)
