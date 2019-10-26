from abc import ABC, abstractmethod
import json

class Serializable:
    """Parent class for all components of adaptive cards.

    Each component should inherit from this class and then specify, from
    its properties, which fall into the following two categories:

    * Simple properties are text properties like "type" or "id"
    * Serializable properties are properties that can themselfes be serilized.
    This includes lists of items (i.e. the 'body' field of the adaptive card) or
    single objects that also inherit from Serializable
    """
    def __init__(self, serializable_properties, simple_properties):
        """Creates a serializable object.

        See class docstring for an explanation what the different types of
        properties are.

        Args:
            serializable_properties(list): List of all serializable properties
            simple_properties(list): List of all simple properties.
        """
        self.serializable_properties = serializable_properties
        self.simple_properties = simple_properties

    def to_json(self, pretty=False):
        """Create json from a serializable component

        This function is used to render the json from a component. While all
        components do support this operation it is mainly used on the
        AdaptiveCard to generate the json for the attachment.

        Args:
            pretty(boolean): If true, the returned json will be sorted by keys
                and indented with 4 spaces to make it more human-readable

        Returns:
            A Json representation of this component
        """
        ret = None
        if pretty:
            ret = json.dumps(self.to_dict(), indent=4, sort_keys=True)
        else:
            ret = json.dumps(self.to_dict())

        return ret

    def to_dict(self):
        """Export a dictionary representation of this card/component by
        parsing all simple and serializable properties.

        A simple_component is a single-text property of the exported card
        (i.e. {'version': "1.2"}) while a serializable property is another
        subcomponent that also implements a to_dict() method.

        The to_dict() method is used to recursively create a dict representation
        of the adaptive card. This dictionary representation can then be
        converted into json for usage with the API.

        Returns:
            dict: Dictionary representation of this component.
        """
        export = {}

        # Export simple properties (i.e. properties that are only single text)
        for sp in self.simple_properties:
            o = getattr(self, sp, None)

            if o is not None:
                export[sp] = str(o)

        # Export all complex properties by calling its respective serialization
        for cp in self.serializable_properties:
            o = getattr(self, cp, None)

            if o is not None:
                # Check if it is a list or a single component
                l = []
                if isinstance(o, list):
                    for i in o:
                        l.append(i.to_dict())
                else:
                    l.append(o.to_dict())
                export[cp] = l

        return export
