"""Webex Adaptive Card - Containers Model.

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
import webexpythonsdk.models.cards.card_elements as CARD_ELEMENTS
import webexpythonsdk.models.cards.inputs as INPUTS
import webexpythonsdk.models.cards.types as TYPES
import webexpythonsdk.models.cards.options as OPTIONS
from webexpythonsdk.models.cards.utils import (
    check_type,
    validate_input,
    validate_dict_str,
    validate_uri,
)


class ActionSet(AdaptiveCardComponent):
    """
    **Adaptive Card - ActionSet Element**

    Displays a set of actions.
    """

    type = "ActionSet"

    def __init__(
        self,
        actions: list[object],
        fallback: object = None,
        height: OPTIONS.BlockElementHeight = None,
        horizontalAlignment: OPTIONS.HorizontalAlignment = None,
        separator: bool = None,
        spacing: OPTIONS.Spacing = None,
        id: str = None,
        isVisible: bool = True,
        requires: dict[str, str] = None,
    ):
        """
        Initialize a new ActionSet element.

        Args:
            actions (list of Action Element(s), Mandatory): The array of
                Action elements to show. Allowed value(s):
                OpenUrl, ShowCard, Submit, ToggleVisibility
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
            horizontalAlignment (HorizontalAlignment, Optional): Controls the
                horizontal alignment of the ColumnSet. When not specified, the
                value of horizontalAlignment is inherited from the parent
                container. If no parent container has horizontalAlignment set,
                it defaults to Left. Allowed value(s):
                HorizontalAlignment.LEFT, HorizontalAlignment.CENTER, or
                HorizontalAlignment.RIGHT
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
            actions,
            (
                ACTIONS.OpenUrl,
                ACTIONS.ShowCard,
                ACTIONS.Submit,
                ACTIONS.ToggleVisibility,
            ),
            is_list=True,
        )

        if hasattr(fallback, "to_dict"):
            check_type(
                fallback,
                (
                    ActionSet,
                    ColumnSet,
                    Container,
                    FactSet,
                    CARD_ELEMENTS.Image,
                    ImageSet,
                    INPUTS.ChoiceSet,
                    INPUTS.Date,
                    INPUTS.Number,
                    INPUTS.Text,
                    INPUTS.Time,
                    INPUTS.Toggle,
                    CARD_ELEMENTS.Media,
                    CARD_ELEMENTS.RichTextBlock,
                    CARD_ELEMENTS.TextBlock,
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

        validate_input(
            horizontalAlignment,
            OPTIONS.HorizontalAlignment,
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
        self.actions = actions
        self.fallback = fallback
        self.height = height
        self.horizontalAlignment = horizontalAlignment
        self.separator = separator
        self.spacing = spacing
        self.id = id
        self.isVisible = isVisible
        self.requires = requires

        super().__init__(
            serializable_properties=[
                "actions",
                *(["fallback"] if hasattr(fallback, "to_dict") else []),
            ],
            simple_properties=[
                "type",
                *([] if hasattr(fallback, "to_dict") else ["fallback"]),
                "height",
                "horizontalAlignment",
                "separator",
                "spacing",
                "id",
                "isVisible",
                "requires",
            ],
        )


class Container(AdaptiveCardComponent):
    """
    **Adaptive Card - Container Element**

    Containers group items together.
    """

    type = "Container"

    def __init__(
        self,
        items: list[object],
        selectAction: object = None,
        style: OPTIONS.ContainerStyle = None,
        verticalContentAlignment: OPTIONS.VerticalContentAlignment = None,
        bleed: bool = None,
        backgroundImage: object = None,
        minHeight: str = None,
        fallback: object = None,
        height: OPTIONS.BlockElementHeight = None,
        horizontalAlignment: OPTIONS.HorizontalAlignment = None,
        separator: bool = None,
        spacing: OPTIONS.Spacing = None,
        id: str = None,
        isVisible: bool = True,
        requires: dict[str, str] = None,
    ):
        """
        Initialize a new Container element.

        Args:
            items (list of Card Element(s), Mandatory): The card elements to
                render inside the Container. Allowed value(s):
                ActionSet, ColumnSet, Container, FactSet, Image, ImageSet,
                ChoiceSet, Date, Number, Text, Time, Toggle, Media,
                RichTextBlock, TextBlock
            selectAction (Action Element, Optional): An Action that will be
                invoked when the Container is tapped or selected.
                Action.ShowCard is not supported. **_Defaults to None._**
                Allowed value(s):
                OpenUrl, Submit, or ToggleVisibility
            style (ContainerStyle, Optional): Style hint for Container.
                **_Defaults to None._**Allowed value(s):
                ContainerStyle.DEFAULT, ContainerStyle.EMPHASIS,
                ContainerStyle.GOOD, ContainerStyle.ATTENTION,
                ContainerStyle.WARNING, or ContainerStyle.ACCENT
            verticalContentAlignment (VerticalContentAlignment, Optional):
                Defines how the content should be aligned vertically within
                the container. When not specified, the value of
                verticalContentAlignment is inherited from the parent
                container. If no parent container has verticalContentAlignment
                set, it defaults to Top. Allowed value(s):
                VerticalContentAlignment.TOP, VerticalContentAlignment.CENTER,
                or VerticalContentAlignment.BOTTOM
            bleed (bool, Optional): Determines whether the element should
                bleed through its parent's padding. **_Defaults to None._**
            backgroundImage (BackgroundImage or uri, Optional): Specifies the
                background image. Acceptable formats are PNG, JPEG, and GIF.
                **_Defaults to None._** Allowed value(s):
                BackgroundImage or uri
            minHeight (str, Optional): Specifies the minimum height of the
                container in pixels, like "80px". **_Defaults to None._**
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
            horizontalAlignment (HorizontalAlignment, Optional): Controls the
                horizontal alignment of the ColumnSet. When not specified, the
                value of horizontalAlignment is inherited from the parent
                container. If no parent container has horizontalAlignment set,
                it defaults to Left. Allowed value(s):
                HorizontalAlignment.LEFT, HorizontalAlignment.CENTER, or
                HorizontalAlignment.RIGHT
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
            items,
            (
                ActionSet,
                ColumnSet,
                Container,
                FactSet,
                CARD_ELEMENTS.Image,
                ImageSet,
                INPUTS.ChoiceSet,
                INPUTS.Date,
                INPUTS.Number,
                INPUTS.Text,
                INPUTS.Time,
                INPUTS.Toggle,
                CARD_ELEMENTS.Media,
                CARD_ELEMENTS.RichTextBlock,
                CARD_ELEMENTS.TextBlock,
            ),
            is_list=True,
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
            style,
            OPTIONS.ContainerStyle,
            optional=True,
        )

        validate_input(
            verticalContentAlignment,
            OPTIONS.VerticalContentAlignment,
            optional=True,
        )

        check_type(
            bleed,
            bool,
            optional=True,
        )

        # Check if backgroundImage is of TYPES.BackgroundImage type
        if hasattr(backgroundImage, "to_dict"):
            check_type(
                backgroundImage,
                TYPES.BackgroundImage,
                optional=True,
            )
        # If not, check if it is an URI and reachable
        else:
            validate_uri(
                backgroundImage,
                optional=True,
            )

        check_type(
            minHeight,
            str,
            optional=True,
        )

        if hasattr(fallback, "to_dict"):
            check_type(
                fallback,
                (
                    ActionSet,
                    ColumnSet,
                    Container,
                    FactSet,
                    CARD_ELEMENTS.Image,
                    ImageSet,
                    INPUTS.ChoiceSet,
                    INPUTS.Date,
                    INPUTS.Number,
                    INPUTS.Text,
                    INPUTS.Time,
                    INPUTS.Toggle,
                    CARD_ELEMENTS.Media,
                    CARD_ELEMENTS.RichTextBlock,
                    CARD_ELEMENTS.TextBlock,
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

        validate_input(
            horizontalAlignment,
            OPTIONS.HorizontalAlignment,
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
        self.items = items
        self.selectAction = selectAction
        self.style = style
        self.verticalContentAlignment = verticalContentAlignment
        self.bleed = bleed
        self.backgroundImage = backgroundImage
        self.minHeight = minHeight
        self.fallback = fallback
        self.height = height
        self.horizontalAlignment = horizontalAlignment
        self.separator = separator
        self.spacing = spacing
        self.id = id
        self.isVisible = isVisible
        self.requires = requires

        super().__init__(
            serializable_properties=[
                "items",
                "selectAction",
                *(
                    ["backgroundImage"]
                    if hasattr(backgroundImage, "to_dict")
                    else []
                ),
                *(["fallback"] if hasattr(fallback, "to_dict") else []),
            ],
            simple_properties=[
                "type",
                "style",
                "verticalContentAlignment",
                "bleed",
                *(
                    []
                    if hasattr(backgroundImage, "to_dict")
                    else ["backgroundImage"]
                ),
                "minHeight",
                *([] if hasattr(fallback, "to_dict") else ["fallback"]),
                "height",
                "separator",
                "spacing",
                "id",
                "isVisible",
                "requires",
            ],
        )


class ColumnSet(AdaptiveCardComponent):
    """
    **Adaptive Card - ColumnSet Element**

    ColumnSet divides a region into Columns, allowing elements to sit
    side-by-side.
    """

    type = "ColumnSet"

    def __init__(
        self,
        columns: list[object] = None,
        selectAction: object = None,
        style: OPTIONS.ContainerStyle = None,
        bleed: bool = None,
        minHeight: str = None,
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
        Initialize a new ColumnSet element.

        Args:
            columns (list of Column Element(s), Optional): The array of
                Columns to divide the region into. **_Defaults to None._**
                Allowed value(s):
                Column
            selectAction (Action Element, Optional): An Action that will be
                invoked when the ColumnSet is tapped or selected.
                Action.ShowCard is not supported. **_Defaults to None._**
                Allowed value(s):
                OpenUrl, Submit, or ToggleVisibility
            style (ContainerStyle, Optional): Style hint for ColumnSet.
                **_Defaults to None._**Allowed value(s):
                ContainerStyle.DEFAULT, ContainerStyle.EMPHASIS,
                ContainerStyle.GOOD, ContainerStyle.ATTENTION,
                ContainerStyle.WARNING, or ContainerStyle.ACCENT
            bleed (bool, Optional): Determines whether the element should
                bleed through its parent's padding. **_Defaults to None._**
            minHeight (str, Optional): Specifies the minimum height of the
                column set in pixels, like "80px". **_Defaults to None._**
            horizontalAlignment (HorizontalAlignment, Optional): Controls the
                horizontal alignment of the ColumnSet. When not specified, the
                value of horizontalAlignment is inherited from the parent
                container. If no parent container has horizontalAlignment set,
                it defaults to Left. Allowed value(s):
                HorizontalAlignment.LEFT, HorizontalAlignment.CENTER, or
                HorizontalAlignment.RIGHT
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
            horizontalAlignment (HorizontalAlignment, Optional): Controls the
                horizontal alignment of the ColumnSet. When not specified, the
                value of horizontalAlignment is inherited from the parent
                container. If no parent container has horizontalAlignment set,
                it defaults to Left. Allowed value(s):
                HorizontalAlignment.LEFT, HorizontalAlignment.CENTER, or
                HorizontalAlignment.RIGHT
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
            columns,
            Column,
            optional=True,
            is_list=True,
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
            style,
            OPTIONS.ContainerStyle,
            optional=True,
        )

        check_type(
            bleed,
            bool,
            optional=True,
        )

        check_type(
            minHeight,
            str,
            optional=True,
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
                    ActionSet,
                    ColumnSet,
                    Container,
                    FactSet,
                    CARD_ELEMENTS.Image,
                    ImageSet,
                    INPUTS.ChoiceSet,
                    INPUTS.Date,
                    INPUTS.Number,
                    INPUTS.Text,
                    INPUTS.Time,
                    INPUTS.Toggle,
                    CARD_ELEMENTS.Media,
                    CARD_ELEMENTS.RichTextBlock,
                    CARD_ELEMENTS.TextBlock,
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
        self.columns = columns
        self.selectAction = selectAction
        self.style = style
        self.bleed = bleed
        self.minHeight = minHeight
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
                "columns",
                "selectAction",
                *(["fallback"] if hasattr(fallback, "to_dict") else []),
            ],
            simple_properties=[
                "type",
                "style",
                "bleed",
                "minHeight",
                "horizontalAlignment",
                *([] if hasattr(fallback, "to_dict") else ["fallback"]),
                "height",
                "horizontalAlignment",
                "separator",
                "spacing",
                "id",
                "isVisible",
                "requires",
            ],
        )


class Column(AdaptiveCardComponent):
    """
    **Adaptive Card - Column Element**

    Defines a container that is part of a ColumnSet.
    """

    type = "Column"

    def __init__(
        self,
        items: list[object] = None,
        backgroundImage: object = None,
        bleed: bool = None,
        fallback: object = None,
        horizontalAlignment: OPTIONS.HorizontalAlignment = None,
        minHeight: str = None,
        separator: bool = None,
        spacing: OPTIONS.Spacing = None,
        selectAction: object = None,
        style: OPTIONS.ContainerStyle = None,
        verticalContentAlignment: OPTIONS.VerticalContentAlignment = None,
        width: object = None,
        id: str = None,
        isVisible: bool = True,
        requires: dict[str, str] = None,
    ):
        """
        Initialize a new Column element.

        Args:
            items (list of Column Element(s), Optional): The card elements to
                render inside the Column. **_Defaults to None._** Allowed
                value(s):
                ActionSet, ColumnSet, Container, FactSet, Image, ImageSet,
                ChoiceSet, Date, Number, Text, Time, Toggle, Media,
                RichTextBlock, TextBlock
            backgroundImage (BackgroundImage or uri, Optional): Specifies the
                background image. Acceptable formats are PNG, JPEG, and GIF.
                **_Defaults to None._** Allowed value(s):
                BackgroundImage or uri
            bleed (bool, Optional): Determines whether the element should
                bleed through its parent's padding. **_Defaults to None._**
            fallback (Column Element or str, Optional): Describes what to do
                when an unknown element is encountered or the requires of this
                or any children can't be met. **_Defaults to None._** Allowed
                value(s):
                Column or "drop".
                Note: "drop" causes this element to be dropped immediately
                when unknown elements are encountered. The unknown element
                doesn't bubble up any higher.
            horizontalAlignment (HorizontalAlignment, Optional): Controls the
                horizontal alignment of the ColumnSet. When not specified, the
                value of horizontalAlignment is inherited from the parent
                container. If no parent container has horizontalAlignment set,
                it defaults to Left. Allowed value(s):
                HorizontalAlignment.LEFT, HorizontalAlignment.CENTER, or
                HorizontalAlignment.RIGHT
            minHeight (str, Optional): Specifies the minimum height of the
                container in pixels, like "80px". **_Defaults to None._**
            separator (bool, Optional): When true, draw a separating line at
                the top of the element. **_Defaults to None._**
            spacing (Spacing, Optional): Controls the amount of spacing
                between this element and the preceding element. **_Defaults to
                None._** Allowed value(s):
                Spacing.DEFAULT, Spacing.NONE, Spacing.SMALL, Spacing.MEDIUM,
                Spacing.LARGE, Spacing.EXTRA_LARGE, or Spacing.PADDING.
            selectAction (Action Element, Optional): An Action that will be
                invoked when the Column is tapped or selected. Action.ShowCard
                is not supported. **_Defaults to None._** Allowed value(s):
                OpenUrl, Submit, or ToggleVisibility
            style (ContainerStyle, Optional): Style hint for Column.
                **_Defaults to None._**Allowed value(s):
                ContainerStyle.DEFAULT, ContainerStyle.EMPHASIS,
                ContainerStyle.GOOD, ContainerStyle.ATTENTION,
                ContainerStyle.WARNING, or ContainerStyle.ACCENT
            verticalContentAlignment (VerticalContentAlignment, Optional):
                Defines how the content should be aligned vertically within
                the column. When not specified, the value of
                verticalContentAlignment is inherited from the parent
                container. If no parent container has verticalContentAlignment
                set, it defaults to Top. **_Defaults to None._** Allowed
                value(s):
                VerticalContentAlignment.TOP, VerticalContentAlignment.CENTER,
                or VerticalContentAlignment.BOTTOM
            width (str or int, Optional): "auto", "stretch", a number
                representing relative width of the column in the column group,
                or in version 1.1 and higher, a specific pixel width, like
                "50px". **_Defaults to None._** Allowed value(s):
                str ("auto" or "stretch") or int
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
            items,
            (
                ActionSet,
                ColumnSet,
                Container,
                FactSet,
                CARD_ELEMENTS.Image,
                ImageSet,
                INPUTS.ChoiceSet,
                INPUTS.Date,
                INPUTS.Number,
                INPUTS.Text,
                INPUTS.Time,
                INPUTS.Toggle,
                CARD_ELEMENTS.Media,
                CARD_ELEMENTS.RichTextBlock,
                CARD_ELEMENTS.TextBlock,
            ),
            optional=True,
            is_list=True,
        )

        # Check if backgroundImage is of TYPES.BackgroundImage type
        if hasattr(backgroundImage, "to_dict"):
            check_type(
                backgroundImage,
                TYPES.BackgroundImage,
                optional=True,
            )
        # If not, check if it is an URI and reachable
        else:
            validate_uri(
                backgroundImage,
                optional=True,
            )

        check_type(
            bleed,
            bool,
            optional=True,
        )

        if hasattr(fallback, "to_dict"):
            check_type(
                fallback,
                Column,
                optional=True,
            )
        else:
            validate_input(
                fallback,
                "drop",
                optional=True,
            )

        validate_input(
            horizontalAlignment,
            OPTIONS.HorizontalAlignment,
            optional=True,
        )

        check_type(
            minHeight,
            str,
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
            selectAction,
            (
                ACTIONS.OpenUrl,
                ACTIONS.Submit,
                ACTIONS.ToggleVisibility,
            ),
            optional=True,
        )

        validate_input(
            style,
            OPTIONS.ContainerStyle,
            optional=True,
        )

        validate_input(
            verticalContentAlignment,
            OPTIONS.VerticalContentAlignment,
            optional=True,
        )

        check_type(
            width,
            (
                str,
                int,
            ),
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
        self.items = items
        self.backgroundImage = backgroundImage
        self.bleed = bleed
        self.fallback = fallback
        self.horizontalAlignment = horizontalAlignment
        self.minHeight = minHeight
        self.separator = separator
        self.spacing = spacing
        self.selectAction = selectAction
        self.style = style
        self.verticalContentAlignment = verticalContentAlignment
        self.width = width
        self.id = id
        self.isVisible = isVisible
        self.requires = requires

        super().__init__(
            serializable_properties=[
                "items",
                *(
                    ["backgroundImage"]
                    if hasattr(backgroundImage, "to_dict")
                    else []
                ),
                *(["fallback"] if hasattr(fallback, "to_dict") else []),
                "selectAction",
            ],
            simple_properties=[
                "type",
                *(
                    []
                    if hasattr(backgroundImage, "to_dict")
                    else ["backgroundImage"]
                ),
                "bleed",
                *([] if hasattr(fallback, "to_dict") else ["fallback"]),
                "horizontalAlignment",
                "minHeight",
                "separator",
                "spacing",
                "style",
                "verticalContentAlignment",
                "width",
                "id",
                "isVisible",
                "requires",
            ],
        )


class FactSet(AdaptiveCardComponent):
    """
    **Adaptive Card - FactSet Element**

    The FactSet element displays a series of facts (i.e., name/value pairs) in
    a tabular form.
    """

    type = "FactSet"

    def __init__(
        self,
        facts: list[object],
        fallback: object = None,
        height: OPTIONS.BlockElementHeight = None,
        separator: bool = None,
        spacing: OPTIONS.Spacing = None,
        id: str = None,
        isVisible: bool = True,
        requires: dict[str, str] = None,
    ):
        """
        Initialize a new FactSet element.

        Args:
            facts (list of Fact Element(s), Mandatory): The array of Fact's.
                Allowed value(s):
                Fact
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
            facts,
            Fact,
            is_list=True,
        )

        if hasattr(fallback, "to_dict"):
            check_type(
                fallback,
                (
                    ActionSet,
                    ColumnSet,
                    Container,
                    FactSet,
                    CARD_ELEMENTS.Image,
                    ImageSet,
                    INPUTS.ChoiceSet,
                    INPUTS.Date,
                    INPUTS.Number,
                    INPUTS.Text,
                    INPUTS.Time,
                    INPUTS.Toggle,
                    CARD_ELEMENTS.Media,
                    CARD_ELEMENTS.RichTextBlock,
                    CARD_ELEMENTS.TextBlock,
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
        self.facts = facts
        self.fallback = fallback
        self.height = height
        self.separator = separator
        self.spacing = spacing
        self.id = id
        self.isVisible = isVisible
        self.requires = requires

        super().__init__(
            serializable_properties=[
                "facts",
                *(["fallback"] if hasattr(fallback, "to_dict") else []),
            ],
            simple_properties=[
                "type",
                *([] if hasattr(fallback, "to_dict") else ["fallback"]),
                "height",
                "separator",
                "id",
                "spacing",
                "isVisible",
                "requires",
            ],
        )


class Fact(AdaptiveCardComponent):
    """
    **Adaptive Card - Fact Element**

    Describes a Fact in a FactSet as a key/value pair.
    """

    def __init__(
        self,
        title: str,
        value: str,
    ):
        """
        Initialize a new Fact element for the FactSet element.

        Args:
            title (str, Mandatory): The title of the fact.
            value (str, Mandatory): The value of the fact.
        """
        # Check types
        check_type(
            title,
            str,
        )

        check_type(
            value,
            str,
        )

        # Set properties
        self.title = title
        self.value = value

        super().__init__(
            serializable_properties=[],
            simple_properties=[
                "title",
                "value",
            ],
        )


class ImageSet(AdaptiveCardComponent):
    """
    **Adaptive Card - ImageSet Element**

    The ImageSet displays a collection of Images similar to a gallery.
    Acceptable formats are PNG, JPEG, and GIF.
    """

    type = "ImageSet"

    def __init__(
        self,
        images: list[object],
        imageSize: OPTIONS.ImageSize = OPTIONS.ImageSize.MEDIUM,
        fallback: object = None,
        height: OPTIONS.BlockElementHeight = None,
        horizontalAlignment: OPTIONS.HorizontalAlignment = None,
        separator: bool = None,
        spacing: OPTIONS.Spacing = None,
        id: str = None,
        isVisible: bool = True,
        requires: dict[str, str] = None,
    ):
        """
        Initialize a new ImageSet element.

        Args:
            images (list of Image Element(s), Mandatory): The array of Image
                elements to show. Allowed value(s):
                Image
            imageSize (ImageSize, Optional): Controls the approximate size of
                each image. The physical dimensions will vary per host. Auto
                and stretch are not supported for ImageSet. The size will
                default to medium if those values are set. **_Defaults to
                ImageSize.MEDIUM._** Allowed value(s):
                ImageSize.AUTO, ImageSize.STRETCH, ImageSize.SMALL,
                ImageSize.MEDIUM, or ImageSize.LARGE
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
            horizontalAlignment (HorizontalAlignment, Optional): Controls the
                horizontal alignment of the ColumnSet. When not specified, the
                value of horizontalAlignment is inherited from the parent
                container. If no parent container has horizontalAlignment set,
                it defaults to Left. Allowed value(s):
                HorizontalAlignment.LEFT, HorizontalAlignment.CENTER, or
                HorizontalAlignment.RIGHT
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
            images,
            CARD_ELEMENTS.Image,
            is_list=True,
        )

        validate_input(
            imageSize,
            OPTIONS.ImageSize,
            optional=True,
        )

        if hasattr(fallback, "to_dict"):
            check_type(
                fallback,
                (
                    ActionSet,
                    ColumnSet,
                    Container,
                    FactSet,
                    CARD_ELEMENTS.Image,
                    ImageSet,
                    INPUTS.ChoiceSet,
                    INPUTS.Date,
                    INPUTS.Number,
                    INPUTS.Text,
                    INPUTS.Time,
                    INPUTS.Toggle,
                    CARD_ELEMENTS.Media,
                    CARD_ELEMENTS.RichTextBlock,
                    CARD_ELEMENTS.TextBlock,
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

        validate_input(
            horizontalAlignment,
            OPTIONS.HorizontalAlignment,
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
        self.images = images
        self.imageSize = imageSize
        self.fallback = fallback
        self.height = height
        self.horizontalAlignment = horizontalAlignment
        self.separator = separator
        self.spacing = spacing
        self.id = id
        self.isVisible = isVisible
        self.requires = requires

        super().__init__(
            serializable_properties=[
                "images",
                *(["fallback"] if hasattr(fallback, "to_dict") else []),
            ],
            simple_properties=[
                "type",
                "imageSize",
                *([] if hasattr(fallback, "to_dict") else ["fallback"]),
                "height",
                "horizontalAlignment",
                "separator",
                "spacing",
                "id",
                "isVisible",
                "requires",
            ],
        )
