# -*- coding: utf-8 -*-
"""Webex Teams Access-Tokens API wrapper.

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

from .abstract_components import Serializable

class Text(Serializable):
    def __init__(self, id, isMultiline=None,
                           maxLength=None,
                           placeholder=None,
                           style=None,
                           value=None,
                           height=None,
                           separator=None,
                           spacing=None):

        self.type = "Input.Text"
        self.id = id
        self.isMultiline = isMultiline
        self.maxLength = maxLength
        self.placeholder = placeholder
        self.style = style
        self.value = value
        self.height = height
        self.separator = separator
        self.spacing = spacing

        super().__init__(serializable_properties=[],
                         simple_properties=[
                            'id', 'type', 'isMultiline', 'maxLength',
                            'placeholder', 'style', 'value', 'height',
                            'separator', 'spacing'
                        ])

class Number(Serializable):
    def __init__(self, id, max=None,
                           min=None,
                           placeholder=None,
                           value=None,
                           height=None,
                           separator=None,
                           spacing=None):
        self.type = "Input.Number"
        self.id = id
        self.max = max
        self.min = min
        self.placeholder = placeholder
        self.value = value
        self.height = height
        self.separator = separator
        self.spacing = spacing

        super().__init__(serializable_properties=[],
                         simple_properties=[
                            'type', 'id', 'max', 'min', 'placeholder', 'value',
                            'height', 'separator', 'spacing'
                         ])

class Date(Serializable):
    def __init__(self, id, max=None,
                           min=None,
                           placeholder=None,
                           value=None,
                           height=None,
                           separator=None,
                           spacing=None):
        self.type = "Input.Date"
        self.id = id
        self.max = max
        self.min = min
        self.placeholder = placeholder
        self.value = value
        self.height = height
        self.separator = separator
        self.spacing = spacing

        super().__init__(serializable_properties=[],
                         simple_properties=[
                            'type', 'id', 'max', 'min', 'placeholder', 'value',
                            'height', 'separator', 'spacing'
                         ])
class Time(Serializable):
    def __init__(self, id, max=None,
                           min=None,
                           placeholder=None,
                           value=None,
                           height=None,
                           separator=None,
                           spacing=None):
        self.id = id
        self.type = "Input.Time"
        self.max = max
        self.min = min
        self.placeholder = placeholder
        self.value = value
        self.height = height
        self.separator = separator
        self.spacing = spacing

        super().__init__(serializable_properties=[],
                         simple_properties=[
                            'id', 'type', 'max', 'min', 'placeholder', 'value',
                            'height', 'separator', 'spacing'
                        ])

class Toggle(Serializable):
    def __init__(self, title, id, value=None,
                                  valueOff=None,
                                  valueOn=None,
                                  height=None,
                                  separator=None,
                                  spacing=None):
        self.title = title
        self.type = "Input.Toggle"
        self.id = id
        self.value = value
        self.valueOff = valueOff
        self.valueOn = valueOn
        self.height = height
        self.separator = separator
        self.spacing = spacing

        super().__init__(serializable_properties=[],
                         simple_properties=[
                            'type', 'id', 'title', 'value', 'valueOff',
                            'valueOn', 'height', 'separator', 'spacing'
                        ])

class Choices(Serializable):
    def __init__(self, choices, id, isMultiSelect=None,
                                    style=None,
                                    value=None,
                                    height=None,
                                    separator=None,
                                    spacing=None):
        self.choices = choices
        self.type = "Input.ChoiceSet"
        self.id = id
        self.isMultiSelect = isMultiSelect
        self.style = style
        self.value = value
        self.height = height
        self.separator = separator
        self.spacing = spacing

        super().__init__(serializable_properties=['choices'],
                         simple_properties=[
                            'id', 'type', 'isMultiSelect', 'style', 'value',
                            'height', 'separator', 'spacing'
                         ])
