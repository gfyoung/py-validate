import functools

__all__ = ["validate_inputs", "validate_outputs"]


def _check_value(arg, val, validator):
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
