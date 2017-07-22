"""
Provides wrapper functions to validate inputs and outputs for functions.

These wrappers work by instantiating a class object that wraps the function
to accept input and output validators that are then used to check inputs and
outputs before and after the function is called respectively.
"""

from py_validate.backend import ValidatedFunction
from py_validate.backend.helpers import DocSubstitution
from py_validate.backend.base import validator_doc, output_len_doc

__all__ = ["validate_inputs", "validate_outputs"]

validator_type_doc = """Each validator can either be a shortcut string, type,
or callable, which is used to check whether the value
supplied for that argument is valid."""


@DocSubstitution(tabs=2, validator_doc=validator_doc,
                 validator_type_doc=validator_type_doc)
def validate_inputs(**validators):
    """
    Wrapper for validating the inputs of a function.

    Parameters
    ----------
    validators : kwargs
        A dictionary mapping argument names to validators.

        {validator_type_doc}

        {validator_doc}

    Returns
    -------
    validator_decorator : callable
        A function decorator that can be used to validate function inputs
        and outputs if decorated with `validate_outputs`.
    """

    def wrapper(f):
        if not isinstance(f, ValidatedFunction):
            f = ValidatedFunction(f)

        f.update_input_validators(**validators)
        return f

    return wrapper


# The output_len_doc parameter documents the `exp_output_len` parameter.
@DocSubstitution(tabs=2, validator_type_doc=validator_type_doc,
                 output_len_doc=(output_len_doc, 1),
                 validator_doc=validator_doc)
def validate_outputs(exp_output_len=None, *validators):
    """
    Wrapper for validating the outputs of a function.

    Parameters
    ----------
    {output_len_doc}

    validators : varargs
        A list of validators to check against arguments returned from a
        function call. It is assumed that the first validator provided
        is to check the first returned element, the second validator
        provided is to check the second returned element, etc.

        {validator_type_doc}

        {validator_doc}

    Returns
    -------
    validator_decorator : callable
        A function decorator that can be used to validate function outputs
        and inputs if decorated with `validate_inputs`.
    """

    def wrapper(f):
        if not isinstance(f, ValidatedFunction):
            f = ValidatedFunction(f)

        f.update_exp_output_len(exp_output_len)
        f.update_output_validators(*validators)

        return f

    return wrapper
