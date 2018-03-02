# -*- coding: utf-8 -*-
"""GeneratorContainer class makes generator functions safe for reuse.

Classes:
    GeneratorContainer: Makes generator functions sage for reuse.

Functions:
    generator_container: Function decorator for wrapping a generator function
        in a GeneratorContainer.

"""


from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from builtins import *
import functools
import inspect
from itertools import islice
import sys


__author__ = "Chris Lunsford"
__author_email__ = "chrlunsf@cisco.com"
__copyright__ = "Copyright (c) 2016-2018 Cisco and/or its affiliates."
__license__ = "MIT"


class GeneratorContainer(object):
    """Store a generator function call, making it for safe reuse.

    Return a fresh generator every time __iter__() is called on the container
    object.

    """

    def __init__(self, generator_function, *args, **kwargs):
        """Init a new GeneratorContainer.

        Args:
            generator_function(func): The generator function.
            *args: The arguments passed to the generator function.
            **kwargs: The keyword arguments passed to the generator function.

        """
        if not inspect.isgeneratorfunction(generator_function):
            raise TypeError("generator_function must be a generator function.")

        self.generator_function = generator_function

        if sys.version_info[0] < 3:
            self.arguments = inspect.getcallargs(
                self.generator_function,
                *args,
                **kwargs
            )
        else:
            signature = inspect.signature(self.generator_function)
            bound_arguments = signature.bind(*args, **kwargs)
            self.arguments = bound_arguments.arguments

    def __repr__(self):
        """A string representation of this object."""
        return '<GeneratorContainer {func_name}({arguments})>'.format(
            func_name=self.generator_function.__qualname__,
            arguments=", ".join(
                str(key) + '=' + repr(value)
                for key, value in self.arguments.items()
            ),
        )

    def __str__(self):
        """A human-readable string representation of this object."""
        return self.__repr__()

    def new_generator(self):
        """Create a new generator object."""
        return self.generator_function(**self.arguments)

    def __iter__(self):
        """Return a fresh iterator."""
        return self.new_generator()

    def __getitem__(self, item):
        """Slice a generator container.

        This is a convenience feature that, with a minor optimization, is
        essentially syntactic sugar for:

        `itertools.islice(GeneratorContainer, start, stop, step)`

        This method attempts to optimize the spark request page size for
        slicing by setting the `max` parameter to the stop-value of the slice.
        If the sliced sequence can be returned in a single response, it will
        be. Otherwise automatic pagination will take care of returning enough
        pages for the data to be sliced.  If `max=` was already specified as a
        parameter to the generator function wrapped by the GeneratorContainer,
        this optimization will not change the value.

        Args:
            item(slice): A slice object specifying the start, stop and step.

        Returns:
            itertools.islice: An itertools.islice object slicing the
                GeneratorContainer's wrapped generator function.

        """
        if isinstance(item, slice):
            arguments = self.arguments.copy()
            arguments.setdefault('max', item.stop)
            return islice(
                self.generator_function(**arguments),
                item.start,
                item.stop,
                item.step,
            )
        else:
            raise IndexError("GeneratorContainers support slicing only. "
                             "Indexing is not supported.")


def generator_container(generator_function):
    """Function Decorator: Containerize calls to a generator function.

    Args:
        generator_function(func): The generator function being containerized.

    Returns:
        func: A wrapper function that containerizes the calls to the generator
            function.

    """

    @functools.wraps(generator_function)
    def generator_container_wrapper(*args, **kwargs):
        """Store a generator call in a container and return the container.

        Args:
            *args: The arguments passed to the generator function.
            **kwargs: The keyword arguments passed to the generator function.

        Returns:
            GeneratorContainer: A container wrapping the call to the generator.

        """
        return GeneratorContainer(generator_function, *args, **kwargs)

    return generator_container_wrapper
