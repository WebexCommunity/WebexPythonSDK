# -*- coding: utf-8 -*-
"""Webex Teams Adaptive Card Component base class.

Copyright (c) 2016-2020 Cisco and/or its affiliates.

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

import json
import enum


class AdaptiveCardComponent:
    """Base class for all Adaptive Card components.

    Each component should inherit from this class and specify which of its
    properties fall into the following two categories:

    * Simple properties are basic types (int, float, str, etc.).

    * Serializable properties are properties that can themselves be serialized.
      This includes lists of items (i.e. the 'body' field of the adaptive card)
      or single objects that also inherit from Serializable
    """
    def __init__(self, serializable_properties, simple_properties):
        """Initialize a serializable object.

        Args:
            serializable_properties(list): List of all serializable properties
            simple_properties(list): List of all simple properties.
        """
        self.serializable_properties = serializable_properties
        self.simple_properties = simple_properties

    def to_dict(self):
        """Serialize the component into a Python dictionary.

        The to_dict() method recursively serializes the object's data into
        a Python dictionary.

        Returns:
            dict: Dictionary representation of this component.
        """
        serialized_data = {}

        # Serialize simple properties
        for property_name in self.simple_properties:
            property_value = getattr(self, property_name, None)

            if property_value is not None:
                if isinstance(property_value, enum.Enum):
                    property_value = str(property_value)

                serialized_data[property_name] = property_value

        # Recursively serialize sub-components
        for property_name in self.serializable_properties:
            property_value = getattr(self, property_name, None)

            if property_value is not None:
                if isinstance(property_value, list):
                    serialized_data[property_name] = [
                        item.to_dict() for item in property_value
                    ]
                else:
                    serialized_data[property_name] = property_value.to_dict()

        return serialized_data

    def to_json(self, **kwargs):
        """Serialize the component into JSON text.

        Any keyword arguments provided are passed through the Python JSON
        encoder.
        """
        return json.dumps(self.to_dict(), **kwargs)
