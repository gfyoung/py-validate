import functools

__all__ = ["validate_inputs", "validate_outputs"]


def _check_value(arg, val, validator):
    """
    Check whether a value provided for an argument is valid.

    Parameters
    ----------
    arg : str
        The name of the argument.
    val : val
        The value of the argument.
    validator : type, callable, or None
        The method to call to validate the argument OR type to check against.

    Raises
    ------
    TypeError : the argument had a type mismatch with `validator`
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

    def outer_wrapper(f):
        var_names = f.__code__.co_varnames

        @functools.wraps(f)
        def inner_wrapper(*args, **kwargs):
            for index, val in enumerate(args):
                # Too many arguments have been provided,
                # but let Python handle this instead of us.
                if index >= len(var_names):
                    break

                var_name = var_names[index]

                if var_name in kwargs:
                    msg = ("{func_name}() got multiple values "
                           "for argument '{arg_name}'")
                    raise TypeError(msg.format(func_name=f.__name__,
                                               arg_name=var_name))

                index += 1
                _check_value(var_name, val, validators.get(var_name))

            for var_name, val in kwargs.items():
                _check_value(var_name, val, validators.get(var_name))

            return f(*args, **kwargs)

        return inner_wrapper

    return outer_wrapper


def validate_outputs(*validators):
    """
    Wrapper for validating the outputs of a function.

    Parameters
    ----------
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

    def outer_wrapper(f):

        @functools.wraps(f)
        def inner_wrapper(*args, **kwargs):
            orig_result = f(*args, **kwargs)

            if not hasattr(orig_result, "__iter__"):
                result = [orig_result]
            else:
                result = orig_result[:]

            for index, validator in enumerate(validators):
                if index >= len(result):
                    break

                val = result[index]
                var_name = "Output {i}".format(i=index)

                _check_value(var_name, val, validator)

            return orig_result

        return inner_wrapper

    return outer_wrapper
