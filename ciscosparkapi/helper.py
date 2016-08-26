"""Package helper functions and classes.

Functions:
    utf8: Returns the input string as a UTF-8 unicode encoded string.
    generator_container: Function decorator that containerizes calls to
        generator functions.

Classes:
    GeneratorContainer: Container for storing a function call to a generator
        function.

"""


import functools


def utf8(string):
    """Return the 'string' as a UTF-8 unicode encoded string.

    Ensure that 'string' is a unicode encoded string; converting if necessary.

    Args:
        string(unicode, str): The input string.

    Returns:
        unicode: The input string encoded as a unicode string.

    Raises:
        AssertionError: If the parameter types are incorrect.

    """
    assert isinstance(string, basestring)
    if isinstance(string, unicode):
        return string
    elif isinstance(string, str):
        return unicode(string, encoding='utf-8')


class GeneratorContainer(object):
    """Container for storing a function call to a generator function.

    Return a fresh iterator every time __iter__() is called on the container
    object.

    Attributes:
        generator(func): The generator function.
        args(list): The arguments passed to the generator function.
        kwargs(dict): The keyword arguments passed to the generator function.

    """

    def __init__(self, generator, *args, **kwargs):
        """Inits a new GeneratorContainer.

        Args:
            generator(func): The generator function.
            *args: The arguments passed to the generator function.
            **kwargs: The keyword arguments passed to the generator function.

        """
        self.generator = generator
        self.args = args
        self.kwargs = kwargs

    def __iter__(self):
        """Return a fresh iterator."""
        return self.generator(*self.args, **self.kwargs)


def generator_container(generator):
    """Function Decorator: Containerize calls to a generator function.

    Args:
        generator(func): The generator function being containerized.

    Returns:
        func: A wrapper function that containerizes the calls to the generator.

    """

    @functools.wraps(generator)
    def generator_container_wrapper(*args, **kwargs):
        """Store a generator call in a container and return the container.

        Args:
            *args: The arguments passed to the generator function.
            **kwargs: The keyword arguments passed to the generator function.

        Returns:
            GeneratorContainer: A container wrapping the call to the generator.

        """
        return GeneratorContainer(generator, *args, **kwargs)

    return generator_container_wrapper
