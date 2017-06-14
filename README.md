[![Build Status](https://travis-ci.org/gfyoung/py-validate.svg?branch=master)](https://travis-ci.org/gfyoung/py-validate)

# py-validate
Function wrappers for verifying Python arguments and return values.

# Examples
Function wrappers nicely abstract away checks on inputs and outputs that can sometimes clutter implementation of the function itself, as illustrated below in this example:

~~~python
def sum_int_float(a, b):
    if not isinstance(a, int):
        raise TypeError("Expected an integer for `a`")

    if not isinstance(b, float):
        raise TypeError("Expected a float for `b`")

    return a + b

>>> sum_int_float(1.5, 1.5)
...
TypeError: Expected an integer for `a`

>>> sum_int_float(1, 1)
...
TypeError: Expected a float for `b`
~~~

Here we just want to sum an integer and a float. However, we have to include these checks for `type` to ensure that our first input is an `int` and that our second input is a `float`. These checks can obfuscate the core functionality, which is just the summation. This example isn't too bad, but now imagine if we had many such functions in our codebase. Our code would be littered with validation checks! Here is the same summation function implemented with our decorators:

~~~python
import py_validate as pv

@pv.validate_inputs(a=int, b=float)
def sum_int_float(a, b):
    return a + b

>>> sum_int_float(1.5, 1.5)
...
TypeError: Incorrect type for variable 'a': expected int but got float instead

>>> sum_int_float(1, 1)
...
TypeError: Incorrect type for variable 'b': expected float but got int instead
~~~

Here, the checks are nicely abstracted away, and we can see exactly what the function is doing assuming valid inputs.

In addition to validating inputs, we also can validate outputs. This can be useful for checking that functions behave as they are supposed to behave:

~~~python
import py_validate as pv

def sum_helper(a, b):
    return a + b

@pv.validate_outputs(2, int)
def sum_int_float(a, b):
    if a == 0:
        # This function doesn't return two outputs
        # as we expect the outer function to.
        return sum_helper(a, b)
    return a, a + b

>>> sum_int_float(0, 1)
...
ValueError: Expected 2 items returned but got 1

>>> sum_int_float(1.5, 1)
...
TypeError: Incorrect type for variable 'Output 0': expected int but got float instead
~~~

These function decorators can also be stacked, which is useful if there are a lot of inputs or outputs to check, as follows:

~~~python
import py_validate as pv

@pv.validate_inputs(a=int)
@pv.validate_inputs(b=float)
@pv.validate_outputs(None, int)
def sum_int_float(a, b):
    return a + b


>>> sum_int_float(1.5, 1.5)
...
TypeError: Incorrect type for variable 'a': expected int but got float instead

>>> sum_int_float(1, 1)
...
TypeError: Incorrect type for variable 'b': expected float but got int instead

>>> sum_int_float(1, 1.5)
...
TypeError: Incorrect type for variable 'Output 0': expected int but got float instead
~~~

This library also comes with some shortcuts that can make it easier to write verification checks:

~~~python
import py_validate as pv

@pv.validate_inputs(a="number")
def increment_input(a):
    return a + 1

>>> increment_input("foo")
...
TypeError: Expected a number but got: 'str'
~~~
