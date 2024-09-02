"""Webex Adaptive Card - Options Model.

Copyright (c) 2016-2024 Cisco and/or its affiliates.

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
    """
    Abstract base class for options represented as strings.
    """

    def __str__(self):
        """Return the string representation of the enum value."""
        return str(self.value)


class FontSize(AbstractOption):
    """
    Enumeration for different font sizes.
    """

    DEFAULT = "default"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    EXTRA_LARGE = "extraLarge"


class FontType(AbstractOption):
    """
    Enumeration for different font types.
    """

    DEFAULT = "default"
    MONOSPACE = "monospace"


class FontWeight(AbstractOption):
    """
    Enumeration for different font weights.
    """

    DEFAULT = "default"
    LIGHTER = "lighter"
    BOLDER = "bolder"


class Colors(AbstractOption):
    """
    Enumeration for different color options.
    """

    DEFAULT = "default"
    DARK = "dark"
    LIGHT = "light"
    ACCENT = "accent"
    GOOD = "good"
    WARNING = "warning"
    ATTENTION = "attention"


class BlockElementHeight(AbstractOption):
    """
    Enumeration for different block element height options.
    """

    AUTO = "auto"
    STRETCH = "stretch"


class VerticalContentAlignment(AbstractOption):
    """
    Enumeration for vertical content alignment options.
    """

    TOP = "top"
    CENTER = "center"
    BOTTOM = "bottom"


class HorizontalAlignment(AbstractOption):
    """
    Enumeration for different horizontal alignment options.
    """

    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"


class Spacing(AbstractOption):
    """
    Enumeration for different spacing options.
    """

    DEFAULT = "default"
    NONE = "none"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    EXTRA_LARGE = "extraLarge"
    PADDING = "padding"


class ImageSize(AbstractOption):
    """
    Enumeration for different image sizes.
    """

    AUTO = "auto"
    STRETCH = "stretch"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


class ImageStyle(AbstractOption):
    """
    Enumeration for different image styles.
    """

    DEFAULT = "default"
    PERSON = "person"


class ContainerStyle(AbstractOption):
    """
    Enumeration for different container styles.
    """

    DEFAULT = "default"
    EMPHASIS = "emphasis"
    GOOD = "good"
    ATTENTION = "attention"
    WARNING = "warning"
    ACCENT = "accent"


class TextInputStyle(AbstractOption):
    """
    Enumeration for different text input styles.
    """

    TEXT = "text"
    TEL = "tel"
    URL = "url"
    EMAIL = "email"


class ChoiceInputStyle(AbstractOption):
    """
    Enumeration for different choice input styles.
    """

    COMPACT = "compact"
    EXPANDED = "expanded"


class ActionStyle(AbstractOption):
    """
    Enumeration for different action stlyes.
    """

    DEFAULT = "default"
    POSITIVE = "positive"
    DESTRUCTIVE = "destructive"


class AssociatedInputs(AbstractOption):
    """
    Enumeration for different associated input options.
    """

    AUTO = "auto"
    NONE = "none"


class ImageFillMode(AbstractOption):
    """
    Enumeration for different image fill modes.
    """

    COVER = "cover"
    REPEAT_HORIZONTALLY = "repeatHorizontally"
    REPEAT_VERTICALLY = "repeatVertically"
    REPEAT = "repeat"
