"""
Base class that underlies the validation wrappers for input and output.
"""

from .shortcuts import mappings


validator_doc = """If a string is provided, that means we are using a shortcut,
which maps to a callable that returns None and raises an
Exception if the validation fails.

If an invalid shortcut is provided, a TypeError will be raised.
Currently, valid shortcuts are:

1) number - The input must be a number.
2) integer - The input must be an integer. This means that type
             of the input must be integral. Thus, "1.0" will fail
             this check even though it is equal to an integer.
3) even - The input must be an even integer.
4) odd - The input must be an odd integer.

If a type is provided, we check if the variable is an instance
of that type, and we raise a TypeError if there is a type mismatch.

If a callable is provided, we expect the callable to return True
(or some equivalent like one) if the check passes and raise OR
return False (or some equivalent like zero) if the check fails."""


class DocSubstitution(object):
    """
    Decorator class for substituting variables in docstring templates.
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
        kwargs : kwargs
            The parameters that we are going to pass into the function
            docstring so that it displays the correct documentation.
        """

        formatted_kwargs = {}

        for param, value in kwargs.items():
            new_lines = [line for line in value.split("\n")]
            new_value = ("\n" + "    " * tabs).join(new_lines)

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


class ValidatedFunction(object):
    """
    Wrapper class around functions for supporting input and output validation.
    """

    def __init__(self, f):
        """
        Initialize a ValidatedFunction instance.

        Parameters
        ----------
        f : callable
            The function that we wish to wrap for validation. We assume that
            we are not passing in another _ValidatedFunction instance.
        """

        self.f = self._validate_callable(f)
        self.var_names = f.__code__.co_varnames

        self._exp_output_len = None
        self._input_validators = {}
        self._output_validators = tuple()

    @staticmethod
    def _validate_callable(f):
        """
        Validate the callable parameter to `_ValidatedFunction`

        Parameters
        ----------
        f : callable
            The callable parameter that we wish to validate.

        Returns
        -------
        orig_f : callable
            The original callable parameter if it is valid.

        Raises
        ------
        TypeError : the callable input is invalid.
        """

        msg = "Invalid function parameter provided"

        valid_callable = callable(f) and hasattr(f, "__code__")
        valid_callable = valid_callable and hasattr(f.__code__, "co_varnames")

        if not valid_callable:
            raise ValueError(msg)

        return f

    def __call__(self, *args, **kwargs):
        """
        Wrapper method around calling `f`.

        Before calling the function, the inputs are validated, and after the
        function is called, the outputs are validated. If all checks pass, the
        output of the function call is returned.
        """

        self._validate_inputs(*args, **kwargs)
        result = self.f(*args, **kwargs)

        if not hasattr(result, "__iter__"):
            self._validate_outputs(result)
        else:
            self._validate_outputs(*result)

        return result

    def update_exp_output_len(self, exp_output_len):
        """
        Update the expected length of the function output.

        Parameters
        ----------
        exp_output_len : int
            The new expected length of the function output.
        """

        if exp_output_len is not None:
            if not isinstance(exp_output_len, int):
                raise TypeError("Expected an integer for "
                                "expected output length")

            if exp_output_len < 0:
                raise ValueError("Expected output length "
                                 "must be positive")

        self._exp_output_len = exp_output_len

    def update_input_validators(self, **validators):
        """
        Update the input validators.

        Parameters
        ----------
        validators : kwargs
            The new input validators to add / update in the existing ones.
        """

        self._input_validators.update(**validators)

    def update_output_validators(self, *validators):
        """
        Update the output validators.

        This function will append new validators to the existing ones.

        Parameters
        ----------
        validators : args
            The new output validators to add to the existing ones.
        """

        self._output_validators = self._output_validators + validators

    @staticmethod
    @DocSubstitution(tabs=3, validator_doc=validator_doc)
    def _check_value(arg, val, validator):
        """
        Check whether a value provided for an argument is valid.

        Parameters
        ----------
        arg : str
            The name of the argument.
        val : object
            The value of the argument.
        validator : str, type, callable, or None
            The method by which to validate the argument.

            {validator_doc}

        Raises
        ------
        TypeError : the argument had a type mismatch with `validator` OR
                    the validator was an invalid one for checking
        ValueError : the `validator` callable failed with `val`
        """

        if validator is None:
            return

        if isinstance(validator, str):
            msg = "Unknown shortcut: '{shortcut}'".format(shortcut=validator)
            validator = mappings.get(validator)

            if validator is not None:
                validator(val)
            else:
                raise ValueError(msg)

        elif isinstance(validator, type):
            if not isinstance(val, validator):
                act_type = type(val).__name__
                exp_type = validator.__name__

                msg = ("Incorrect type for variable '{inp_name}': "
                       "expected {exp_type} but got {act_type} instead")
                raise TypeError(msg.format(inp_name=arg,
                                           exp_type=exp_type,
                                           act_type=act_type))
        elif callable(validator):
            is_valid = validator(val)

            if is_valid is False:
                msg = ("Invalid value for variable "
                       "'{inp_name}': {val}")
                raise ValueError(msg.format(inp_name=arg, val=val))

        else:
            validator_type = type(validator).__name__
            raise TypeError("Validator must either be a shortcut, "
                            "callable, or type, not {v_type}"
                            .format(v_type=validator_type))

    def _validate_inputs(self, *args, **kwargs):
        """
        Validate the inputs to a function.
        """

        for index, val in enumerate(args):
            # Too many arguments have been provided,
            # but let Python handle this instead of us.
            if index >= len(self.var_names):
                break

            var_name = self.var_names[index]

            if var_name in kwargs:
                msg = ("{func_name}() got multiple values "
                       "for argument '{arg_name}'")
                raise TypeError(msg.format(func_name=self.f.__name__,
                                           arg_name=var_name))

            index += 1

            validator = self._input_validators.get(var_name)
            self._check_value(var_name, val, validator)

        for var_name, val in kwargs.items():
            validator = self._input_validators.get(var_name)
            self._check_value(var_name, val, validator)

    def _validate_outputs(self, *args):
        """
        Validate the outputs of a function.
        """

        if self._exp_output_len is not None:
            if self._exp_output_len != len(args):
                raise ValueError(
                    "Expected {exp_count} items returned but "
                    "got {act_count}".format(exp_count=self._exp_output_len,
                                             act_count=len(args)))

        for index, validator in enumerate(self._output_validators):
            if index >= len(args):
                break

            val = args[index]
            var_name = "Output {i}".format(i=index)

            self._check_value(var_name, val, validator)
