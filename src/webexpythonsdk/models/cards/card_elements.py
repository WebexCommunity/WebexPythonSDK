"""Webex Adaptive Card - Card Elements Model.

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
import webexpythonsdk.models.cards.actions as ACTIONS
import webexpythonsdk.models.cards.containers as CONTAINERS
import webexpythonsdk.models.cards.inputs as INPUTS
import webexpythonsdk.models.cards.options as OPTIONS
from webexpythonsdk.models.cards.utils import (
    check_type,
    validate_input,
    validate_dict_str,
    validate_uri,
)


class TextBlock(AdaptiveCardComponent):
    """
    **Adaptive Card - TextBlock Element**

    Displays text, allowing control over font sizes, weight, and color.
    """

    type = "TextBlock"

    def __init__(
        self,
        text: str,
        color: OPTIONS.Colors = None,
        fontType: OPTIONS.FontType = None,
        horizontalAlignment: OPTIONS.HorizontalAlignment = None,
        isSubtle: bool = None,
        maxLines: int = None,
        size: OPTIONS.FontSize = None,
        weight: OPTIONS.FontWeight = None,
        wrap: bool = None,
        fallback: object = None,
        height: OPTIONS.BlockElementHeight = None,
        separator: bool = None,
        spacing: OPTIONS.Spacing = None,
        id: str = None,
        isVisible: bool = True,
        requires: dict[str, str] = None,
    ):
        """
        Initialize a new TextBlock element.

        Args:
            text (str, Mandatory): Text to display.
            color (Colors, Optional): Control the color of TextBlock element.
                **_Defaults to None._** Allowed value(s):
                Colors.DEFAULT, Colors.DARK, Colors.LIGHT, Colors.ACCENT,
                Colors.GOOD, Colors.WARNING, or Colors.ATTENTION.
            fontType (FontType, Optional): Type of font to use for rendering.
                **_Defaults to None._** Allowed value(s):
                FontType.DEFAULT or FontType.MONOSPACE.
            horizontalAlignment (HorizontalAlignment, Optional): Controls the
                horizontal text alignment. When not specified, the value of
                horizontalAlignment is inherited from the parent container. If
                no parent container has horizontalAlignment set, it defaults
                to Left. Allowed value(s):
                HorizontalAlignment.LEFT, HorizontalAlignment.CENTER, or
                HorizontalAlignment.RIGHT.
            isSubtle (bool, Optional): If true, displays text slightly toned
                down to appear less prominent. **_Defaults to None._**
            maxLines (int, Optional): Specifies the maximum number of lines to
                display. **_Defaults to None._**
            size (FontSize, Optional): Controls size of text. **_Defaults to
                None._** Allowed value(s):
                FontSize.DEFAULT, FontSize.SMALL, FontSize.MEDIUM,
                FontSize.LARGE, or FontSize.EXTRA_LARGE.
            weight (FontWeight, Optional): Controls the weight of TextBlock
                elements. **_Defaults to None._** Allowed value(s):
                FontWeight.DEFAULT, FontWeight.LIGHTER, or FontWeight.BOLDER.
            wrap (bool, Optional): If true, allow text to wrap. Otherwise,
                text is clipped. **_Defaults to None._**
            fallback (Element or str, Optional): Describes what to do when an
                unknown element is encountered or the requires of this or any
                children can't be met. **_Defaults to None._** Allowed
                value(s):
                ActionSet, ColumnSet, Container, FactSet, Image, ImageSet,
                ChoiceSet, Date, Number, Text, Time, Toggle, Media,
                RichTextBlock, TextBlock, or "drop".
                Note: "drop" causes this element to be dropped immediately
                when unknown elements are encountered. The unknown element
                doesn't bubble up any higher.
            height (BlockElementHeight, Optional): Specifies the height of the
                element. **_Defaults to None._** Allowed value(s):
                BlockElementHeight.AUTO or BlockElementHeight.STRETCH
            separator (bool, Optional): When true, draw a separating line at
                the top of the element. **_Defaults to None._**
            spacing (Spacing, Optional): Controls the amount of spacing
                between this element and the preceding element. **_Defaults to
                None._** Allowed value(s):
                Spacing.DEFAULT, Spacing.NONE, Spacing.SMALL, Spacing.MEDIUM,
                Spacing.LARGE, Spacing.EXTRA_LARGE, or Spacing.PADDING.
            id (str, Optional): A unique identifier associated with the item.
                **_Defaults to None._**
            isVisible (bool, Optional): If false, this item will be removed
                from the visual tree. **_Defaults to True._**
            requires (Dictionary(string), Optional): A series of key/value
                pairs indicating features that the item requires with
                corresponding minimum version. When a feature is missing or of
                insufficient version, fallback is triggered. In the Dictionary,
                both key(s) and value(s) should be of str datatype. **_Defaults
                to None._**
        """
        # Check types
        check_type(
            text,
            str,
        )

        validate_input(
            color,
            OPTIONS.Colors,
            optional=True,
        )

        validate_input(
            fontType,
            OPTIONS.FontType,
            optional=True,
        )

        validate_input(
            horizontalAlignment,
            OPTIONS.HorizontalAlignment,
            optional=True,
        )

        check_type(
            isSubtle,
            bool,
            optional=True,
        )

        check_type(
            maxLines,
            int,
            optional=True,
        )

        validate_input(
            size,
            OPTIONS.FontSize,
            optional=True,
        )

        validate_input(
            weight,
            OPTIONS.FontWeight,
            optional=True,
        )

        check_type(
            wrap,
            bool,
            optional=True,
        )

        if hasattr(fallback, "to_dict"):
            check_type(
                fallback,
                (
                    CONTAINERS.ActionSet,
                    CONTAINERS.ColumnSet,
                    CONTAINERS.Container,
                    CONTAINERS.FactSet,
                    Image,
                    CONTAINERS.ImageSet,
                    INPUTS.ChoiceSet,
                    INPUTS.Date,
                    INPUTS.Number,
                    INPUTS.Text,
                    INPUTS.Time,
                    INPUTS.Toggle,
                    Media,
                    RichTextBlock,
                    TextBlock,
                ),
                optional=True,
            )
        else:
            validate_input(
                fallback,
                "drop",
                optional=True,
            )

        validate_input(
            height,
            OPTIONS.BlockElementHeight,
            optional=True,
        )

        check_type(
            separator,
            bool,
            optional=True,
        )

        validate_input(
            spacing,
            OPTIONS.Spacing,
            optional=True,
        )

        check_type(
            id,
            str,
            optional=True,
        )

        check_type(
            isVisible,
            bool,
            optional=True,
        )

        validate_dict_str(
            requires,
            str,
            str,
            optional=True,
        )

        # Set properties
        self.text = text
        self.color = color
        self.fontType = fontType
        self.horizontalAlignment = horizontalAlignment
        self.isSubtle = isSubtle
        self.maxLines = maxLines
        self.size = size
        self.weight = weight
        self.wrap = wrap
        self.fallback = fallback
        self.height = height
        self.separator = separator
        self.spacing = spacing
        self.id = id
        self.isVisible = isVisible
        self.requires = requires

        super().__init__(
            serializable_properties=[
                *(["fallback"] if hasattr(fallback, "to_dict") else []),
            ],
            simple_properties=[
                "type",
                "text",
                "color",
                "fontType",
                "horizontalAlignment",
                "isSubtle",
                "maxLines",
                "size",
                "weight",
                "wrap",
                *([] if hasattr(fallback, "to_dict") else ["fallback"]),
                "height",
                "separator",
                "spacing",
                "id",
                "isVisible",
                "requires",
            ],
        )


class Image(AdaptiveCardComponent):
    """
    **Adaptive Card - Image Element**

    Displays an image. Acceptable formats are PNG, JPEG, and GIF.
    """

    type = "Image"

    def __init__(
        self,
        url: object,
        altText: str = None,
        backgroundColor: str = None,
        height: object = OPTIONS.BlockElementHeight.AUTO,
        horizontalAlignment: OPTIONS.HorizontalAlignment = None,
        selectAction: object = None,
        size: OPTIONS.ImageSize = None,
        style: OPTIONS.ImageStyle = None,
        width: str = None,
        fallback: object = None,
        separator: bool = None,
        spacing: OPTIONS.Spacing = None,
        id: str = None,
        isVisible: bool = True,
        requires: dict[str, str] = None,
    ):
        """
        Initialize a new Image element.

        Args:
            url (str, Mandatory): The URL to the image. Supports data URI.
                Allowed value(s):
                uri
            altText (str, Optional): Alternate text describing the image.
                **_Defaults to None._**
            backgroundColor (str, Optional): Applies a background to a
                transparent image. This property will respect the image style.
                **_Defaults to None._**
            height (str or BlockElementHeight, Optional): The desired height
                of the image. If specified as a pixel value, ending in 'px',
                E.g., 50px, the image will distort to fit that exact height.
                This overrides the size property. **_Defaults to
                BlockElementHeight.AUTO_** Allowed value(s):
                str, BlockElementHeight.AUTO, or BlockElementHeight.STRETCH
            horizontalAlignment (HorizontalAlignment, Optional): Controls how
                this element is horizontally positioned within its parent.
                When not specified, the value of horizontalAlignment is
                inherited from the parent container. If no parent container
                has horizontalAlignment set, it defaults to Left. Allowed
                value(s):
                HorizontalAlignment.LEFT, HorizontalAlignment.CENTER, or
                HorizontalAlignment.RIGHT.
            selectAction (Action Element, Optional): An Action that will be
                invoked when the Image is tapped or selected. Action.ShowCard
                is not supported. **_Defaults to None._** Allowed value(s):
                OpenUrl, Submit, or ToggleVisibility
            size (ImageSize, Optional): Controls how this Image is displayed.
                **_Defaults to None._** Allowed value(s):
                ImageSize.AUTO, ImageSize.STRETCH, ImageSize.SMALL,
                ImageSize.MEDIUM, or ImageSize.LARGE.
            style (ImageStyle, Optional): Controls the approximate size of the
                image. The physical dimensions will vary per host. **_Defaults
                to None._** Allowed value(s):
                ImageStyle.DEFAULT or ImageStyle.PERSON
            width (str, Optional): The desired on-screen width of the image,
                ending in 'px'. E.g., 50px. This overrides the size property.
                **_Defaults to None._**
            fallback (Element or str, Optional): Describes what to do when an
                unknown element is encountered or the requires of this or any
                children can't be met. **_Defaults to None._** Allowed
                value(s):
                ActionSet, ColumnSet, Container, FactSet, Image, ImageSet,
                ChoiceSet, Date, Number, Text, Time, Toggle, Media,
                RichTextBlock, TextBlock, or "drop".
                Note: "drop" causes this element to be dropped immediately
                when unknown elements are encountered. The unknown element
                doesn't bubble up any higher.
            separator (bool, Optional): When true, draw a separating line at
                the top of the element. **_Defaults to None._**
            spacing (Spacing, Optional): Controls the amount of spacing
                between this element and the preceding element. **_Defaults to
                None._** Allowed value(s):
                Spacing.DEFAULT, Spacing.NONE, Spacing.SMALL, Spacing.MEDIUM,
                Spacing.LARGE, Spacing.EXTRA_LARGE, or Spacing.PADDING.
            id (str, Optional): A unique identifier associated with the item.
                **_Defaults to None._**
            isVisible (bool, Optional): If false, this item will be removed
                from the visual tree. **_Defaults to True._**
            requires (Dictionary(string), Optional): A series of key/value
                pairs indicating features that the item requires with
                corresponding minimum version. When a feature is missing or of
                insufficient version, fallback is triggered. In the Dictionary,
                both key(s) and value(s) should be of str datatype. **_Defaults
                to None._**
        """
        # Check types
        validate_uri(
            url,
        )

        check_type(
            altText,
            str,
            optional=True,
        )

        check_type(
            backgroundColor,
            str,
            optional=True,
        )

        check_type(
            height,
            (
                str,
                OPTIONS.BlockElementHeight,
            ),
            optional=True,
        )

        validate_input(
            horizontalAlignment,
            OPTIONS.HorizontalAlignment,
            optional=True,
        )

        check_type(
            selectAction,
            (
                ACTIONS.OpenUrl,
                ACTIONS.Submit,
                ACTIONS.ToggleVisibility,
            ),
            optional=True,
        )

        validate_input(
            size,
            OPTIONS.ImageSize,
            optional=True,
        )

        validate_input(
            style,
            OPTIONS.ImageStyle,
            optional=True,
        )

        check_type(
            width,
            str,
            optional=True,
        )

        if hasattr(fallback, "to_dict"):
            check_type(
                fallback,
                (
                    CONTAINERS.ActionSet,
                    CONTAINERS.ColumnSet,
                    CONTAINERS.Container,
                    CONTAINERS.FactSet,
                    Image,
                    CONTAINERS.ImageSet,
                    INPUTS.ChoiceSet,
                    INPUTS.Date,
                    INPUTS.Number,
                    INPUTS.Text,
                    INPUTS.Time,
                    INPUTS.Toggle,
                    Media,
                    RichTextBlock,
                    TextBlock,
                ),
                optional=True,
            )
        else:
            validate_input(
                fallback,
                "drop",
                optional=True,
            )

        check_type(
            separator,
            bool,
            optional=True,
        )

        validate_input(
            spacing,
            OPTIONS.Spacing,
            optional=True,
        )

        check_type(
            id,
            str,
            optional=True,
        )

        check_type(
            isVisible,
            bool,
            optional=True,
        )

        validate_dict_str(
            requires,
            str,
            str,
            optional=True,
        )

        # Set properties
        self.url = url
        self.altText = altText
        self.backgroundColor = backgroundColor
        self.height = height
        self.horizontalAlignment = horizontalAlignment
        self.selectAction = selectAction
        self.size = size
        self.style = style
        self.width = width
        self.fallback = fallback
        self.separator = separator
        self.spacing = spacing
        self.id = id
        self.isVisible = isVisible
        self.requires = requires

        super().__init__(
            serializable_properties=[
                "selectAction",
                *(["fallback"] if hasattr(fallback, "to_dict") else []),
            ],
            simple_properties=[
                "type",
                "url",
                "altText",
                "backgroundColor",
                "height",
                "horizontalAlignment",
                "size",
                "style",
                "width",
                *([] if hasattr(fallback, "to_dict") else ["fallback"]),
                "separator",
                "spacing",
                "id",
                "isVisible",
                "requires",
            ],
        )


class Media(AdaptiveCardComponent):
    """
    **Adaptive Card - Media Element**

    Displays a media player for audio or video content.
    """

    type = "Media"

    def __init__(
        self,
        sources: list[object],
        poster: object = None,
        altText: str = None,
        fallback: object = None,
        height: OPTIONS.BlockElementHeight = None,
        separator: bool = None,
        spacing: OPTIONS.Spacing = None,
        id: str = None,
        isVisible: bool = True,
        requires: dict[str, str] = None,
    ):
        """
        Initialize a new Media element.

        Args:
            sources (list of MediaSource Element(s), Mandatory): Array of
                media sources to attempt to play. Allowed value(s):
                MediaSource
            poster (uri, Optional): URL of an image to display before playing.
                Supports data URI. If poster is omitted, the Media element
                will either use a default poster (controlled by the host
                application) or will attempt to automatically pull the poster
                from the target video service when the source URL points to a
                video from a Web provider such as YouTube. **_Defaults to
                None._** Allowed value(s):
                uri
            altText (str, Optional): Alternate text describing the audio or
                video. **_Defaults to None._**
            fallback (Element or str, Optional): Describes what to do when an
                unknown element is encountered or the requires of this or any
                children can't be met. **_Defaults to None._** Allowed
                value(s):
                ActionSet, ColumnSet, Container, FactSet, Image, ImageSet,
                ChoiceSet, Date, Number, Text, Time, Toggle, Media,
                RichTextBlock, TextBlock, or "drop".
                Note: "drop" causes this element to be dropped immediately
                when unknown elements are encountered. The unknown element
                doesn't bubble up any higher.
            height (BlockElementHeight, Optional): Specifies the height of the
                element. **_Defaults to None._** Allowed value(s):
                BlockElementHeight.AUTO or BlockElementHeight.STRETCH
            separator (bool, Optional): When true, draw a separating line at
                the top of the element. **_Defaults to None._**
            spacing (Spacing, Optional): Controls the amount of spacing
                between this element and the preceding element. **_Defaults to
                None._** Allowed value(s):
                Spacing.DEFAULT, Spacing.NONE, Spacing.SMALL, Spacing.MEDIUM,
                Spacing.LARGE, Spacing.EXTRA_LARGE, or Spacing.PADDING.
            id (str, Optional): A unique identifier associated with the item.
                **_Defaults to None._**
            isVisible (bool, Optional): If false, this item will be removed
                from the visual tree. **_Defaults to True._**
            requires (Dictionary(string), Optional): A series of key/value
                pairs indicating features that the item requires with
                corresponding minimum version. When a feature is missing or of
                insufficient version, fallback is triggered. In the Dictionary,
                both key(s) and value(s) should be of str datatype. **_Defaults
                to None._**
        """
        # Check types
        check_type(
            sources,
            MediaSource,
            is_list=True,
        )

        validate_uri(
            poster,
            optional=True,
        )

        check_type(
            altText,
            str,
            optional=True,
        )

        if hasattr(fallback, "to_dict"):
            check_type(
                fallback,
                (
                    CONTAINERS.ActionSet,
                    CONTAINERS.ColumnSet,
                    CONTAINERS.Container,
                    CONTAINERS.FactSet,
                    Image,
                    CONTAINERS.ImageSet,
                    INPUTS.ChoiceSet,
                    INPUTS.Date,
                    INPUTS.Number,
                    INPUTS.Text,
                    INPUTS.Time,
                    INPUTS.Toggle,
                    Media,
                    RichTextBlock,
                    TextBlock,
                ),
                optional=True,
            )
        else:
            validate_input(
                fallback,
                "drop",
                optional=True,
            )

        validate_input(
            height,
            OPTIONS.BlockElementHeight,
            optional=True,
        )

        check_type(
            separator,
            bool,
            optional=True,
        )

        validate_input(
            spacing,
            OPTIONS.Spacing,
            optional=True,
        )

        check_type(
            id,
            str,
            optional=True,
        )

        check_type(
            isVisible,
            bool,
            optional=True,
        )

        validate_dict_str(
            requires,
            str,
            str,
            optional=True,
        )

        # Set properties
        self.sources = sources
        self.poster = poster
        self.altText = altText
        self.fallback = fallback
        self.height = height
        self.separator = separator
        self.spacing = spacing
        self.id = id
        self.isVisible = isVisible
        self.requires = requires

        super().__init__(
            serializable_properties=[
                "sources",
                *(["fallback"] if hasattr(fallback, "to_dict") else []),
            ],
            simple_properties=[
                "type",
                "poster",
                "altText",
                *([] if hasattr(fallback, "to_dict") else ["fallback"]),
                "height",
                "separator",
                "spacing",
                "id",
                "isVisible",
                "requires",
            ],
        )


class MediaSource(AdaptiveCardComponent):
    """
    **Adaptive Card - MediaSource Element**

    Defines a source for a Media element.
    """

    def __init__(
        self,
        url: object,
        mimeType: str = None,
    ):
        """
        Initialize a new MediaSource element.

        Args:
            url (uri, Mandatory): URL to media. Supports data URI. Allowed
                value(s):
                uri
            mimeType (str, Optional): Mime type of associated media
                (e.g. "video/mp4"). For YouTube and other Web video URLs,
                mimeType can be omitted.
        """
        # Check types
        validate_uri(
            url,
        )

        check_type(
            mimeType,
            str,
        )

        # Set properties
        self.url = url
        self.mimeType = mimeType

        super().__init__(
            serializable_properties=[],
            simple_properties=[
                "url",
                "mimeType",
            ],
        )


class RichTextBlock(AdaptiveCardComponent):
    """
    **Adaptive Card - RichTextBlock Element**

    Defines an array of inlines, allowing for inline text formatting.
    """

    type = "RichTextBlock"

    def __init__(
        self,
        inlines: list[object],
        horizontalAlignment: OPTIONS.HorizontalAlignment = None,
        fallback: object = None,
        height: OPTIONS.BlockElementHeight = None,
        separator: bool = None,
        spacing: OPTIONS.Spacing = None,
        id: str = None,
        isVisible: bool = True,
        requires: dict[str, str] = None,
    ):
        """
        Initialize a new RichTextBlock element.

        Args:
            inlines (list of TextRun Card Element(s) or str, Mandatory): The
                array of inlines. Allowed value(s):
                TextRun, str
            horizontalAlignment (HorizontalAlignment, Optional): Controls the
                horizontal text alignment. When not specified, the value of
                horizontalAlignment is inherited from the parent container. If
                no parent container has horizontalAlignment set, it defaults
                to Left. Allowed value(s): HorizontalAlignment.LEFT,
                HorizontalAlignment.CENTER, or HorizontalAlignment.RIGHT
            fallback (Element or str, Optional): Describes what to do when an
                unknown element is encountered or the requires of this or any
                children can't be met. **_Defaults to None._** Allowed
                value(s):
                ActionSet, ColumnSet, Container, FactSet, Image, ImageSet,
                ChoiceSet, Date, Number, Text, Time, Toggle, Media,
                RichTextBlock, TextBlock, or "drop".
                Note: "drop" causes this element to be dropped immediately
                when unknown elements are encountered. The unknown element
                doesn't bubble up any higher.
            height (BlockElementHeight, Optional): Specifies the height of the
                element. **_Defaults to None._** Allowed value(s):
                BlockElementHeight.AUTO or BlockElementHeight.STRETCH
            separator (bool, Optional): When true, draw a separating line at
                the top of the element. **_Defaults to None._**
            spacing (Spacing, Optional): Controls the amount of spacing
                between this element and the preceding element. **_Defaults to
                None._** Allowed value(s):
                Spacing.DEFAULT, Spacing.NONE, Spacing.SMALL, Spacing.MEDIUM,
                Spacing.LARGE, Spacing.EXTRA_LARGE, or Spacing.PADDING.
            id (str, Optional): A unique identifier associated with the item.
                **_Defaults to None._**
            isVisible (bool, Optional): If false, this item will be removed
                from the visual tree. **_Defaults to True._**
            requires (Dictionary(string), Optional): A series of key/value
                pairs indicating features that the item requires with
                corresponding minimum version. When a feature is missing or of
                insufficient version, fallback is triggered. In the Dictionary,
                both key(s) and value(s) should be of str datatype. **_Defaults
                to None._**
        """
        # Check types
        check_type(
            inlines,
            (
                TextRun,
                str,
            ),
            is_list=True,
        )

        validate_input(
            horizontalAlignment,
            OPTIONS.HorizontalAlignment,
            optional=True,
        )

        if hasattr(fallback, "to_dict"):
            check_type(
                fallback,
                (
                    CONTAINERS.ActionSet,
                    CONTAINERS.ColumnSet,
                    CONTAINERS.Container,
                    CONTAINERS.FactSet,
                    Image,
                    CONTAINERS.ImageSet,
                    INPUTS.ChoiceSet,
                    INPUTS.Date,
                    INPUTS.Number,
                    INPUTS.Text,
                    INPUTS.Time,
                    INPUTS.Toggle,
                    Media,
                    RichTextBlock,
                    TextBlock,
                ),
                optional=True,
            )
        else:
            validate_input(
                fallback,
                "drop",
                optional=True,
            )

        validate_input(
            height,
            OPTIONS.BlockElementHeight,
            optional=True,
        )

        check_type(
            separator,
            bool,
            optional=True,
        )

        validate_input(
            spacing,
            OPTIONS.Spacing,
            optional=True,
        )

        check_type(
            id,
            str,
            optional=True,
        )

        check_type(
            isVisible,
            bool,
            optional=True,
        )

        validate_dict_str(
            requires,
            str,
            str,
            optional=True,
        )

        # Set properties
        self.inlines = inlines
        self.horizontalAlignment = horizontalAlignment
        self.fallback = fallback
        self.height = height
        self.separator = separator
        self.spacing = spacing
        self.id = id
        self.isVisible = isVisible
        self.requires = requires

        super().__init__(
            serializable_properties=[
                "inlines",
                *(["fallback"] if hasattr(fallback, "to_dict") else []),
            ],
            simple_properties=[
                "type",
                "horizontalAlignment",
                *([] if hasattr(fallback, "to_dict") else ["fallback"]),
                "height",
                "separator",
                "spacing",
                "id",
                "isVisible",
                "requires",
            ],
        )


class TextRun(AdaptiveCardComponent):
    """
    **Adaptive Card - TextRun Element**

    Defines a single run of formatted text. A TextRun with no properties set
    can be represented in the json as string containing the text as a shorthand
    for the json object. These two representations are equivalent.
    """

    type = "TextRun"

    def __init__(
        self,
        text: str,
        color: OPTIONS.Colors = None,
        fontType: OPTIONS.FontType = None,
        highlight: bool = None,
        isSubtle: bool = None,
        italic: bool = None,
        selectAction: object = None,
        size: OPTIONS.FontSize = None,
        strikethrough: bool = None,
        underline: bool = None,
        weight: OPTIONS.FontWeight = None,
    ):
        """
        Initialize a new TextRun element.

        Args:
            text (str, Mandatory): Text to display. Markdown is not supported.
            color (Colors, Optional): Controls the color of the text.
                **_Defaults to None._** Allowed value(s):
                Colors.DEFAULT, Colors.DARK, Colors.LIGHT, Colors.ACCENT,
                Colors.GOOD, Colors.WARNING, or Colors.ATTENTION
            fontType (FontType, Optional): The type of font to use.
                **_Defaults to None._** Allowed value(s):
                FontType.DEFAULT or FontType.MONOSPACE
            highlight (bool, Optional): If true, displays the text highlighted.
                **_Defaults to None._**
            isSubtle (bool, Optional): If true, displays text slightly toned
                down to appear less prominent. **_Defaults to None._**
            italic (bool, Optional): If true, displays the text using italic
                font. **_Defaults to None._**
            selectAction (Action Element, Optional): Action to invoke when
                this text run is clicked. Visually changes the text run into a
                hyperlink. Action.ShowCard is not supported. **_Defaults to
                None._** Allowed value(s):
                OpenUrl, Submit, or ToggleVisibility
            size (FontSize, Optional): Controls size of text. **_Defaults to
                None._** Allowed value(s):
                FontSize.DEFAULT, FontSize.SMALL, FontSize.MEDIUM,
                FontSize.LARGE, or FontSize.EXTRA_LARGE
            strikethrough (bool, Optional): If true, displays the text with
                strikethrough. **_Defaults to None._**
            underline (bool, Optional): If true, displays the text with an
                underline. **_Defaults to None._**
            weight (FontWeight, Optional): Controls the weight of the text.
                **_Defaults to None._** Allowed value(s):
                FontWeight.DEFAULT, FontWeight.LIGHTER, or FontWeight.BOLDER
        """
        # Check types
        check_type(
            text,
            str,
        )

        validate_input(
            color,
            OPTIONS.Colors,
            optional=True,
        )

        validate_input(
            fontType,
            OPTIONS.FontType,
            optional=True,
        )

        check_type(
            highlight,
            bool,
            optional=True,
        )

        check_type(
            isSubtle,
            bool,
            optional=True,
        )

        check_type(
            italic,
            bool,
            optional=True,
        )

        check_type(
            selectAction,
            (
                ACTIONS.OpenUrl,
                ACTIONS.Submit,
                ACTIONS.ToggleVisibility,
            ),
            optional=True,
        )

        validate_input(
            size,
            OPTIONS.FontSize,
            optional=True,
        )

        check_type(
            strikethrough,
            bool,
            optional=True,
        )

        check_type(
            underline,
            bool,
            optional=True,
        )

        validate_input(
            weight,
            OPTIONS.FontWeight,
            optional=True,
        )

        # Set properties
        self.text = text
        self.color = color
        self.fontType = fontType
        self.highlight = highlight
        self.isSubtle = isSubtle
        self.italic = italic
        self.selectAction = selectAction
        self.size = size
        self.strikethrough = strikethrough
        self.underline = underline
        self.weight = weight

        super().__init__(
            serializable_properties=[
                "selectAction",
            ],
            simple_properties=[
                "type",
                "text",
                "color",
                "fontType",
                "highlight",
                "isSubtle",
                "italic",
                "size",
                "strikethrough",
                "underline",
                "weight",
            ],
        )
