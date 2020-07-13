# -*- coding: utf-8 -*-
"""Webex Teams Adaptive Card options.

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

from enum import Enum


class AbstractOption(Enum):
    def __str__(self):
        return str(self.value)


class FontSize(AbstractOption):
    DEFAULT = "default"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    EXTRA_LARGE = "extraLarge"


class FontWeight(AbstractOption):
    DEFAULT = "default"
    LIGHTER = "lighter"
    BOLDER = "bolder"


class Colors(AbstractOption):
    DEFAULT = "default"
    DARK = "dark"
    LIGHT = "light"
    ACCENT = "accent"
    GOOD = "good"
    WARNING = "warning"
    ATTENTION = "attention"


class BlockElementHeight(AbstractOption):
    AUTO = "auto"
    STRETCH = "auto"


class VerticalContentAlignment(AbstractOption):
    TOP = "top"
    CENTER = "center"
    BOTTOM = "bottom"


class HorizontalAlignment(AbstractOption):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"


class Spacing(AbstractOption):
    DEFAULT = "default"
    NONE = "none"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    EXTRA_LARGE = "extraLarge"
    PADDING = "padding"


class ImageSize(AbstractOption):
    AUTO = "auto"
    STRETCH = "stretch"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


class ImageStyle(AbstractOption):
    DEFAULT = "default"
    PERSON = "person"


class ContainerStyle(AbstractOption):
    DEFAULT = "default"
    EMPHASIS = "emphasis"


class TextInputStyle(AbstractOption):
    TEXT = "text"
    TEL = "tel"
    URL = "url"
    EMAIL = "email"


class ChoiceInputStyle(AbstractOption):
    COMPACT = "compact"
    EXPANDED = "expanded"
