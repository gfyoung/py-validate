[![Build Status](https://travis-ci.org/gfyoung/py-validate.svg?branch=master)](https://travis-ci.org/gfyoung/py-validate)

# py-validate
Function wrappers for verifying Python arguments and return values.

# Installation
You can just install via `pip`:
~~~
pip install py_validate
~~~

Alternatively, you can download the source code and in the top directory of the code, run either:
~~~
pip install .
~~~
or
~~~
python setup.py install
~~~

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

This library also comes with some shortcuts that can make it easier to write verification checks.
The following examples illustrate how to use each of the available shortcuts, which are:

* **number**: the value must be a number
* **integer**: the value must be an integer
* **even**: the value must be an even integer
* **odd**: the value must be an odd integer

~~~python
import py_validate as pv

@pv.validate_inputs(a="number")  # The input must be a number.
def increment_input(a):
    return a + 1

>>> increment_input("foo")
...
TypeError: Expected a number but got: 'str'

>>> increment_input(1.5)
2.5

@pv.validate_inputs(a="integer")  # The input must be an integer by type.
def increment_input_two(a):
    return a + 1

>>> increment_input_two("foo")
...
TypeError: Expected an integer but got: 'str'

>>> increment_input_two(1.5)
...
TypeError: Expected an integer but got: 'float'

>>> increment_input_two(1.0)  # The type is float.
...
TypeError: Expected an integer but got: 'float'

>>> increment_input_two(2)
3

@pv.validate_inputs(a="even")  # The input must be an even integer.
def increment_input_three(a):
    return a + 1

>>> increment_input_three("foo")
...
TypeError: Expected an integer but got: 'str'

>>> increment_input_three(1.5)
...
TypeError: Expected an integer but got: 'float'

>>> increment_input_three(1.0)  # The type is float.
...
TypeError: Expected an integer but got: 'float'

>>> increment_input_three(1)
...
ValueError: Expected an even integer

>>> increment_input_three(2)
3

@pv.validate_inputs(a="odd")  # The input must be an odd integer.
def increment_input_four(a):
    return a + 1

>>> increment_input_four("foo")
...
TypeError: Expected an integer but got: 'str'

>>> increment_input_four(1.5)
...
TypeError: Expected an integer but got: 'float'

>>> increment_input_four(1.0)  # The type is float.
...
TypeError: Expected an integer but got: 'float'

>>> increment_input_four(2)
...
ValueError: Expected an odd integer

>>> increment_input_four(1)
2
~~~

When specifying validators for input variables, do note that once validators for a variable
have been set, they cannot be changed. Doing so will cause an error to be raised:

~~~python
import py_validate as pv

@pv.validate_inputs(a=int)
@pv.validate_inputs(a=float)
def increment_input_five(a):
    return a + 1
...
ValueError : Validator(s) for input 'a' already set.
~~~

Finally, if your function happens to return multiple output variables, the default is to
evaluate each element of the returned tuple. If you want the actual tuple object to be
validated, pass in `-1` for the expected output length:

~~~python
import py_validate as pv

@pv.validate_outputs(-1, tuple)
def return_tuple_if_one(a):
    if a == 1:
        return tuple()
    else:
        return "foo"

>>> return_tuple_if_one(0)
...
TypeError: Incorrect type for variable 'Output 0': expected tuple but got str instead
~~~
