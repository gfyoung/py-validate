"""
Provides wrapper functions to validate inputs and outputs for functions.

This wrappers work by instantiating a class object that wraps the function
to accept input and output validators that are then used to check inputs and
outputs before and after the function is called respectively.
"""

__all__ = ["validate_inputs", "validate_outputs"]


class _ValidatedFunction(object):

    def __init__(self, f):
        """
        Initialize a _ValidatedFunction instance.

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

        if not (exp_output_len is None or isinstance(exp_output_len, int)):
            raise TypeError("Expected an integer for expected output length")

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
    def _check_value(arg, val, validator):
        """
        Check whether a value provided for an argument is valid.

        Parameters
        ----------
        arg : str
            The name of the argument.
        val : object
            The value of the argument.
        validator : type, callable, or None
            The method to call to validate the argument OR type to check.

        Raises
        ------
        TypeError : the argument had a type mismatch with `validator` OR
                    the validator was an invalid one for checking
        ValueError : the `validator` callable failed with `val`
        """

        if validator is None:
            return

        if isinstance(validator, type):
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
            raise TypeError("Validator must either be a callable or "
                            "type, not {v_type}".format(v_type=validator_type))

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


def validate_inputs(**validators):
    """
    Wrapper for validating the inputs of a function.

    Parameters
    ----------
    validators : kwargs
        A dictionary mapping argument names to validators. Each validator
        can either be a type or callable, which be used to check whether
        the value supplied for that argument is valid.

    Returns
    -------
    input_validator_decorator : callable
        A function decorator that can be used to validate function inputs.
    """

    def wrapper(f):
        if not isinstance(f, _ValidatedFunction):
            f = _ValidatedFunction(f)

        f.update_input_validators(**validators)
        return f

    return wrapper


def validate_outputs(exp_len=None, *validators):
    """
    Wrapper for validating the outputs of a function.

    Parameters
    ----------
    exp_len : int
        The expected number of elements in the result.

    validators : varargs
        A list of validators to check against arguments returned from a
        function call. It is assumed that the first validator provided
        is to check the first returned element, the second validator provided
        is to check the second returned element, etc.

    Returns
    -------
    output_validator_decorator : callable
        A function decorator that can be used to validate function outputs.
    """

    def wrapper(f):
        if not isinstance(f, _ValidatedFunction):
            f = _ValidatedFunction(f)

        f.update_exp_output_len(exp_len)
        f.update_output_validators(*validators)

        return f

    return wrapper
