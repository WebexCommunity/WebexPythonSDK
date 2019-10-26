from abc import ABC, abstractmethod
import json

class Serializable:
    """Parent class to

    """
    def __init__(self, serializable_properties, simple_properties):
        self.serializable_properties = serializable_properties
        self.simple_properties = simple_properties

    def to_json(self, pretty=False):
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

class Component:
    def __init__(self, component_type):
        self.component_type = component_type

    def get_type(self):
        return self.component_type
