# -*- coding: utf-8 -*-
"""GeneratorContainer class makes generator functions safe for reuse.

Classes:
    GeneratorContainer: Makes generator functions sage for reuse.

Functions:
    generator_container: Function decorator for wrapping a generator function
        in a GeneratorContainer.

Copyright (c) 2016-2019 Cisco and/or its affiliates.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import functools
import inspect
import sys
import asyncio

# https://stackoverflow.com/questions/42378566/python-3-6-async-version-of-islice
async def aenumerate(aiterable):
    i = 0
    async for x in aiterable:
        yield i, x
        i += 1


async def aislice(aiterable, *args):
    s = slice(*args)
    it = iter(range(s.start or 0, s.stop or sys.maxsize, s.step or 1))
    try:
        nexti = next(it)
    except StopIteration:
        return
    async for i, element in aenumerate(aiterable):
        if i == nexti:
            yield element
            try:
                nexti = next(it)
            except StopIteration:
                return


class AsyncGeneratorContainer(object):
    """Store a generator function call, making it for safe reuse.

    Return a fresh generator every time __aiter__() is called on the container
    object.

    """

    def __init__(self, generator_function, *args, **kwargs):
        """Init a new GeneratorContainer.

        Args:
            generator_function(func): The generator function.
            *args: The arguments passed to the generator function.
            **kwargs: The keyword arguments passed to the generator function.

        """
        if not inspect.isasyncgenfunction(generator_function):
            raise TypeError("generator_function must be an async generator function.")

        self.generator_function = generator_function

        signature = inspect.signature(self.generator_function)
        bound_arguments = signature.bind(*args, **kwargs)
        self.arguments = bound_arguments.arguments
        self._iter = None

    def __repr__(self):
        """A string representation of this object."""
        return "<AsyncGeneratorContainer {func_name}({arguments})>".format(
            func_name=self.generator_function.__name__,
            arguments=", ".join(
                str(key) + "=" + repr(value) for key, value in self.arguments.items()
            ),
        )

    def __str__(self):
        """A human-readable string representation of this object."""
        return self.__repr__()

    def new_generator(self):
        """Create a new generator object."""

        return self.generator_function(**self.arguments)

    def __aiter__(self):
        """Return a fresh iterator."""
        return self.new_generator()

    def __getitem__(self, item):
        """Slice a generator container.

        This is a convenience feature that, with a minor optimization, is
        essentially syntactic sugar for:

        `itertools.islice(GeneratorContainer, start, stop, step)`

        This method attempts to optimize the Webex Teams request page size for
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
            arguments.setdefault("max", item.stop)
            return aislice(
                self.generator_function(**arguments), item.start, item.stop, item.step,
            )
        else:
            raise IndexError(
                "AsyncGeneratorContainers support slicing only. "
                "Indexing is not supported."
            )


def async_generator_container(generator_function):
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
        return AsyncGeneratorContainer(generator_function, *args, **kwargs)

    return generator_container_wrapper
