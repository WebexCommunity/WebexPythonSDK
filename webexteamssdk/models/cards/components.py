# -*- coding: utf-8 -*-
"""Webex Teams Adaptive Card components.

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

from .actions import OpenUrl, Submit
from .adaptive_card_component import AdaptiveCardComponent
from .options import BlockElementHeight, ImageSize, ImageStyle, Spacing
from .utils import check_type


class MediaSource(AdaptiveCardComponent):
    """Adaptive Card Media Source."""

    def __init__(self, mimeType, url):
        """Initialize a new Media Source component.

        Args:
            mimeType(str): Mime type of the associated media(i.e. 'video/mp4')
            url(str): URL of the media.
        """
        # Check types
        check_type(mimeType, str)
        check_type(url, str)

        self.mimeType = mimeType
        self.url = url

        super().__init__(
            serializable_properties=[],
            simple_properties=['mimeType', 'url'],
        )


class Media(AdaptiveCardComponent):
    """Adaptive Card Media component."""
    type = "Media"

    def __init__(self, sources, poster=None, altText=None, height=None,
                 separator=None, spacing=None, id=None):
        """Initialize a new Media component.

        Args:
            sources(list): A list of media sources to be played
            poster(str): The url to the image that is displayed before playing
            altText(str): Alternative text for this component
            height(BlockElementHeight): The height of this block element
            separator(bool): Draw a separating line when set to true
            spacing(Spacing): Specify the spacing of this component
            id(str): The id of this component
        """
        # Check types
        check_type(sources, MediaSource, is_list=True)
        check_type(poster, str, optional=True)
        check_type(altText, str, optional=True)
        check_type(height, BlockElementHeight, optional=True)
        check_type(separator, bool, optional=True)
        check_type(spacing, Spacing, optional=True)
        check_type(id, str, optional=True)

        self.sources = sources
        self.poster = poster
        self.altText = altText
        self.height = height
        self.separator = separator
        self.spacing = spacing
        self.id = id

        super().__init__(
            serializable_properties=['sources'],
            simple_properties=[
                'type', 'poster', 'altText', 'height', 'separator', 'spacing',
                'id',
            ],
        )


class Image(AdaptiveCardComponent):
    """Adaptive Card Image component."""
    type = "Image"

    def __init__(self, url, altText=None, backgroundColor=None, height=None,
                 horizontalAlignment=None, selectAction=None, size=None,
                 style=None, width=None, separator=None, spacing=None,
                 id=None):
        """Initialize a new image component.

        Args:
            url(str): The URL to the image
            altText(str): Alternative text describing the image
            backgroundColor(str): Background color for transparent images.
            height(str, BlockElementHeight): Height of the image either as a
                pixel value(i.e. '50px') or as an instance of
                BlockElementHeight
            horizontalAlignmnet(HorizontalAlignment): Controls how the
                component is positioned within its parent.
            selectAction(OpenUrl, Submit): Option that is carried out when the
                card is selected.
            size(ImageSize): Controls the approximate size of the image.
            style(ImageStyle): The display style of this image.
            width(str): Width of the image as a pixel value (i.e. '50px')
            separator(bool): Draw a separating line when set to true
            spacing(Spacing): Specify the spacing of this component
            id(str): The id of this component
        """
        check_type(url, str)
        check_type(altText, str, optional=True)
        check_type(backgroundColor, str, optional=True)
        check_type(height, (str, BlockElementHeight), optional=True)
        check_type(horizontalAlignment, horizontalAlignment, optional=True)
        check_type(selectAction, (OpenUrl, Submit), optional=True)
        check_type(size, ImageSize, optional=True)
        check_type(style, ImageStyle, optional=True)
        check_type(width, str, optional=True)
        check_type(separator, bool, optional=True)
        check_type(spacing, Spacing, optional=True)
        check_type(id, str, optional=True)

        self.url = url
        self.altText = altText
        self.backgroundColor = backgroundColor
        self.height = height
        self.horizontalAlignment = horizontalAlignment
        self.selectAction = selectAction
        self.size = size
        self.style = style
        self.width = width
        self.separator = separator
        self.spacing = spacing
        self.id = id

        super().__init__(
            serializable_properties=[],
            simple_properties=[
                'type', 'url', 'altText', 'backgroundColor', 'height',
                'horizontalAlignment', 'selectAction', 'size', 'style',
                'width', 'separator', 'spacing', 'id',
            ],
        )


class TextBlock(AdaptiveCardComponent):
    """Adaptive Card Text Block component."""
    type = "TextBlock"

    def __init__(self, text, color=None, horizontalAlignment=None,
                 isSubtle=None, maxLines=None, size=None, weight=None,
                 wrap=None, separator=None, spacing=None, id=None):
        """Initialize a new TextBlock component."""
        # TODO: Document arguments
        self.text = text
        self.color = color
        self.horizontalAlignment = horizontalAlignment
        self.isSubtle = isSubtle
        self.maxLines = maxLines
        self.size = size
        self.weight = weight
        self.wrap = wrap
        self.separator = separator
        self.spacing = spacing
        self.id = id

        super().__init__(
            serializable_properties=[],
            simple_properties=[
                'type', 'text', 'color', 'horizontalAlignment', 'isSubtle',
                'maxLines', 'size', 'weight', 'wrap', 'spacing', 'id',
                'separator',
            ],
        )


class Column(AdaptiveCardComponent):
    """Adaptive Card Column component."""
    type = "Column"

    def __init__(self, items=None, separator=None, spacing=None,
                 selectAction=None, style=None, verticalContentAlignment=None,
                 width=None, id=None):
        """Initialize a new Column component."""
        # TODO: Document arguments
        self.items = items
        self.separator = separator
        self.spacing = spacing
        self.selectAction = selectAction
        self.style = style
        self.verticalContentAlignment = verticalContentAlignment
        self.width = width
        self.id = id

        super().__init__(
            serializable_properties=['items'],
            simple_properties=[
                'type', 'separator', 'spacing', 'selectAction', 'style',
                'verticalContentAlignment', 'width', 'id',
            ],
        )


class Fact(AdaptiveCardComponent):
    """Adaptive Card Fact component."""

    def __init__(self, title, value):
        """Initialize a new Fact component."""
        # TODO: Document arguments
        self.title = title
        self.value = value

        super().__init__(
            serializable_properties=[],
            simple_properties=['title', 'value'],
        )


class Choice(AdaptiveCardComponent):
    def __init__(self, title, value):
        """Initialize a new Choice component."""
        # TODO: Document arguments
        self.title = title
        self.value = value

        super().__init__(
            serializable_properties=[],
            simple_properties=['title', 'value'],
        )
