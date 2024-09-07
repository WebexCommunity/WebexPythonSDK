"""Webex Adaptive Card - Types Model.

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

from webexpythonsdk.models.cards.adaptive_card_component import (
    AdaptiveCardComponent,
)
import webexpythonsdk.models.cards.options as OPTIONS
from webexpythonsdk.models.cards.utils import (
    validate_input,
    validate_uri,
)


class BackgroundImage(AdaptiveCardComponent):
    """
    **Adaptive Card - Background Image Element**

    Specifies a background image. Acceptable formats are PNG, JPEG, and GIF.
    """

    def __init__(
        self,
        url: object,
        fillMode: OPTIONS.ImageFillMode = None,
        horizontalAlignment: OPTIONS.HorizontalAlignment = None,
        verticalAlignment: OPTIONS.VerticalContentAlignment = None,
    ):
        """
        Initialize a new BackgroundImage element.

        Args:
            url (uri, Mandatory): The URL (or data url) of the image.
                Acceptable formats are PNG, JPEG, and GIF. Allowed value(s):
                uri
            fillMode (ImageFillMode, Optional): Describes how the image should
                fill the area. **_Defaults to None._** Allowed value(s):
                ImageFillMode.COVER, ImageFillMode.REPEAT_HORIZONTALLY,
                ImageFillMode.REPEAT_VERTICALLY, or ImageFillMode.REPEAT
            horizontalAlignment (HorizontalAlignment, Optional): Describes how
                the image should be aligned if it must be cropped or if using
                repeat fill mode. **_Defaults to None._** Allowed value(s):
                HorizontalAlignment.LEFT, HorizontalAlignment.CENTER, or
                HorizontalAlignment.RIGHT
            verticalAlignment (VerticalContentAlignment, Optional): Describes
                how the image should be aligned if it must be cropped or if
                using repeat fill mode. **_Defaults to None._** Allowed
                value(s):
                VerticalContentAlignment.TOP, VerticalContentAlignment.CENTER,
                or VerticalContentAlignment.BOTTOM
        """
        # Check types
        validate_uri(
            url,
        )

        validate_input(
            fillMode,
            OPTIONS.ImageFillMode,
            optional=True,
        )

        validate_input(
            horizontalAlignment,
            OPTIONS.HorizontalAlignment,
            optional=True,
        )

        validate_input(
            verticalAlignment,
            OPTIONS.VerticalContentAlignment,
            optional=True,
        )

        # Set properties
        self.url = url
        self.fillMode = fillMode
        self.horizontalAlignment = horizontalAlignment
        self.verticalAlignment = verticalAlignment

        super().__init__(
            serializable_properties=[],
            simple_properties=[
                "url",
                "fillMode",
                "horizontalAlignment",
                "verticalAlignment",
            ],
        )
