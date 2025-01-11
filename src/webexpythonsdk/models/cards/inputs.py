"""Webex Adaptive Card - Inputs Model.

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
import webexpythonsdk.models.cards.containers as CONTAINERS
import webexpythonsdk.models.cards.options as OPTIONS
from webexpythonsdk.models.cards.utils import (
    check_type,
    validate_input,
    validate_dict_str,
)


class Text(AdaptiveCardComponent):
    """
    **Adaptive Card - Input.Text Element**

    Lets a user enter text.
    """

    type = "Input.Text"

    def __init__(
        self,
        id: str,
        isMultiline: bool = None,
        maxLength: int = None,
        placeholder: str = None,
        regex: str = None,
        style: OPTIONS.TextInputStyle = None,
        inlineAction: object = None,
        value: str = None,
        errorMessage: str = None,
        isRequired: bool = None,
        label: str = None,
        fallback: object = None,
        height: OPTIONS.BlockElementHeight = None,
        separator: bool = None,
        spacing: OPTIONS.Spacing = None,
        isVisible: bool = True,
        requires: dict[str, str] = None,
    ):
        """
        Initialize a new Input.Text element.

        Args:
            id (str, Mandatory): Unique identifier for the value. Used to
                identify collected input when the Submit action is performed.
            isMultiline (bool, Optional): If true, allow multiple lines of
                input. **_Defaults to None_.**
            maxLength (int, Optional): Hint of maximum length characters to
                collect (may be ignored by some clients). **_Defaults to
                None_.**
            placeholder (str, Optional): Description of the input desired.
                Displayed when no text has been input. **_Defaults to None_.**
            regex (str, Optional): Regular expression indicating the required
                format of this text input. **_Defaults to None_.**
            style (TextInputStyle, to None_.** Allowed value(s):
                TextInputStyle.TEXT, TextInputStyle.TEL, TextInputStyle.URL, or
                TextInputStyle.EMAIL
            inlineAction (Action Element, Optional): The inline action for the
                input. Typically displayed to the right of the input. It is
                strongly recommended to provide an icon on the action (which
                will be displayed instead of the title of the action).
                **_Defaults to None_.** Allowed value(s):
                OpenUrl, Submit, or ToggleVisibility
            value (str, Optional): The initial value for this field.
                **_Defaults to None_.**
            errorMessage (str, Optional): Error message to display when
                entered input is invalid. **_Defaults to None_.**
            isRequired (bool, Optional): Whether or not this input is required.
                **_Defaults to None_.**
            label (str, Optional): Label for this input. **_Defaults to
                None_.**
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
            id,
            str,
        )

        check_type(
            isMultiline,
            bool,
            optional=True,
        )

        check_type(
            maxLength,
            int,
            optional=True,
        )

        check_type(
            placeholder,
            str,
            optional=True,
        )

        check_type(
            regex,
            str,
            optional=True,
        )

        validate_input(
            style,
            OPTIONS.TextInputStyle,
            optional=True,
        )

        check_type(
            inlineAction,
            (
                ACTIONS.OpenUrl,
                ACTIONS.Submit,
                ACTIONS.ToggleVisibility,
            ),
            optional=True,
        )

        check_type(
            value,
            str,
            optional=True,
        )

        check_type(
            errorMessage,
            str,
            optional=True,
        )

        check_type(
            isRequired,
            bool,
            optional=True,
        )

        check_type(
            label,
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
                    CARD_ELEMENTS.Image,
                    CONTAINERS.ImageSet,
                    ChoiceSet,
                    Date,
                    Number,
                    Text,
                    Time,
                    Toggle,
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
        self.id = id
        self.isMultiline = isMultiline
        self.maxLength = maxLength
        self.placeholder = placeholder
        self.regex = regex
        self.style = style
        self.inlineAction = inlineAction
        self.value = value
        self.errorMessage = errorMessage
        self.isRequired = isRequired
        self.label = label
        self.fallback = fallback
        self.height = height
        self.separator = separator
        self.spacing = spacing
        self.isVisible = isVisible
        self.requires = requires

        super().__init__(
            serializable_properties=[
                "inlineAction",
                *(["fallback"] if hasattr(fallback, "to_dict") else []),
            ],
            simple_properties=[
                "type",
                "id",
                "isMultiline",
                "maxLength",
                "placeholder",
                "regex",
                "style",
                "value",
                "errorMessage",
                "isRequired",
                "label",
                *([] if hasattr(fallback, "to_dict") else ["fallback"]),
                "height",
                "separator",
                "spacing",
                "isVisible",
                "requires",
            ],
        )


class Number(AdaptiveCardComponent):
    """
    **Adaptive Card - Input.Number Element**

    Allows a user to enter a number.
    """

    type = "Input.Number"

    def __init__(
        self,
        id: str,
        max: int = None,
        min: int = None,
        placeholder: str = None,
        value: int = None,
        errorMessage: str = None,
        isRequired: bool = None,
        label: str = None,
        fallback: object = None,
        height: OPTIONS.BlockElementHeight = None,
        separator: bool = None,
        spacing: OPTIONS.Spacing = None,
        isVisible: bool = True,
        requires: dict[str, str] = None,
    ):
        """
        Initialize a new Input.Number element.

        Args:
            id (str, Mandatory): Unique identifier for the value. Used to
                identify collected input when the Submit action is performed.
            max (int, Optional): Hint of maximum value (may be ignored by some
                clients). **_Defaults to None_.**
            min (int, Optional): Hint of minimum value (may be ignored by some
                clients). **_Defaults to None_.**
            placeholder (str, Optional): Description of the input desired.
                Displayed when no text has been input. **_Defaults to None_.**
            value (int, Optional): Initial value for this field. **_Defaults to
                None_.**
            errorMessage (str, Optional): Error message to display when
                entered input is invalid. **_Defaults to None_.**
            isRequired (bool, Optional): Whether or not this input is required.
                **_Defaults to None_.**
            label (str, Optional): Label for this input. **_Defaults to
                None_.**
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
            id,
            str,
        )

        check_type(
            max,
            int,
            optional=True,
        )

        check_type(
            min,
            int,
            optional=True,
        )

        check_type(
            placeholder,
            str,
            optional=True,
        )

        check_type(
            value,
            int,
            optional=True,
        )

        check_type(
            errorMessage,
            str,
            optional=True,
        )

        check_type(
            isRequired,
            bool,
            optional=True,
        )

        check_type(
            label,
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
                    CARD_ELEMENTS.Image,
                    CONTAINERS.ImageSet,
                    ChoiceSet,
                    Date,
                    Number,
                    Text,
                    Time,
                    Toggle,
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
        self.id = id
        self.max = max
        self.min = min
        self.placeholder = placeholder
        self.value = value
        self.errorMessage = errorMessage
        self.isRequired = isRequired
        self.label = label
        self.fallback = fallback
        self.height = height
        self.separator = separator
        self.spacing = spacing
        self.isVisible = isVisible
        self.requires = requires

        super().__init__(
            serializable_properties=[
                *(["fallback"] if hasattr(fallback, "to_dict") else []),
            ],
            simple_properties=[
                "type",
                "id",
                "max",
                "min",
                "placeholder",
                "value",
                "errorMessage",
                "isRequired",
                "label",
                *([] if hasattr(fallback, "to_dict") else ["fallback"]),
                "height",
                "separator",
                "spacing",
                "isVisible",
                "requires",
            ],
        )


class Date(AdaptiveCardComponent):
    """
    **Adaptive Card - Input.Date Element**

    Lets a user choose a date.
    """

    type = "Input.Date"

    def __init__(
        self,
        id: str,
        max: str = None,
        min: str = None,
        placeholder: str = None,
        value: str = None,
        errorMessage: str = None,
        isRequired: bool = None,
        label: str = None,
        fallback: object = None,
        height: OPTIONS.BlockElementHeight = None,
        separator: bool = None,
        spacing: OPTIONS.Spacing = None,
        isVisible: bool = True,
        requires: dict[str, str] = None,
    ):
        """
        Initialize a new Input.Date element.

        Args:
            id (str, Mandatory): Unique identifier for the value. Used to
                identify collected input when the Submit action is performed.
            max (str, Optional): Hint of maximum value expressed in YYYY-MM-DD
                (may be ignored by some clients). **_Defaults to None_.**
            min (str, Optional): Hint of minimum value expressed in YYYY-MM-DD
                (may be ignored by some clients). **_Defaults to None_.**
            placeholder (str, Optional): Description of the input desired.
                Displayed when no text has been input. **_Defaults to None_.**
            value (str, Optional): The initial value for this field expressed
                in YYYY-MM-DD. **_Defaults to None_.**
            errorMessage (str, Optional): Error message to display when
                entered input is invalid. **_Defaults to None_.**
            isRequired (bool, Optional): Whether or not this input is required.
                **_Defaults to None_.**
            label (str, Optional): Label for this input. **_Defaults to
                None_.**
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
            id,
            str,
        )

        check_type(
            max,
            str,
            optional=True,
        )

        check_type(
            min,
            str,
            optional=True,
        )

        check_type(
            placeholder,
            str,
            optional=True,
        )

        check_type(
            value,
            str,
            optional=True,
        )

        check_type(
            errorMessage,
            str,
            optional=True,
        )

        check_type(
            isRequired,
            bool,
            optional=True,
        )

        check_type(
            label,
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
                    CARD_ELEMENTS.Image,
                    CONTAINERS.ImageSet,
                    ChoiceSet,
                    Date,
                    Number,
                    Text,
                    Time,
                    Toggle,
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
        self.id = id
        self.max = max
        self.min = min
        self.placeholder = placeholder
        self.value = value
        self.errorMessage = errorMessage
        self.isRequired = isRequired
        self.label = label
        self.fallback = fallback
        self.height = height
        self.separator = separator
        self.spacing = spacing
        self.isVisible = isVisible
        self.requires = requires

        super().__init__(
            serializable_properties=[
                *(["fallback"] if hasattr(fallback, "to_dict") else []),
            ],
            simple_properties=[
                "type",
                "id",
                "max",
                "min",
                "placeholder",
                "value",
                "errorMessage",
                "isRequired",
                "label",
                *([] if hasattr(fallback, "to_dict") else ["fallback"]),
                "height",
                "separator",
                "spacing",
                "isVisible",
                "requires",
            ],
        )


class Time(AdaptiveCardComponent):
    """
    **Adaptive Card - Input.Time Element**

    Lets a user select a time.
    """

    type = "Input.Time"

    def __init__(
        self,
        id: str,
        max: str = None,
        min: str = None,
        placeholder: str = None,
        value: str = None,
        errorMessage: str = None,
        isRequired: bool = None,
        label: str = None,
        fallback: object = None,
        height: OPTIONS.BlockElementHeight = None,
        separator: bool = None,
        spacing: OPTIONS.Spacing = None,
        isVisible: bool = True,
        requires: dict[str, str] = None,
    ):
        """
        Initialize a new Input.Time element.

        Args:
            id (str, Mandatory): Unique identifier for the value. Used to
                identify collected input when the Submit action is performed.
            max (str, Optional): Hint of maximum value expressed in HH:MM (may
                be ignored by some clients). **_Defaults to None_.**
            min (str, Optional): Hint of minimum value expressed in HH:MM (may
                be ignored by some clients). **_Defaults to None_.**
            placeholder (str, Optional): Description of the input desired.
                Displayed when no text has been input. **_Defaults to None_.**
            value (str, Optional): The initial value for this field expressed
                in HH:MM. **_Defaults to None_.**
            errorMessage (str, Optional): Error message to display when
                entered input is invalid. **_Defaults to None_.**
            isRequired (bool, Optional): Whether or not this input is required.
                **_Defaults to None_.**
            label (str, Optional): Label for this input. **_Defaults to
                None_.**
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
            id,
            str,
        )

        check_type(
            max,
            str,
            optional=True,
        )

        check_type(
            min,
            str,
            optional=True,
        )

        check_type(
            placeholder,
            str,
            optional=True,
        )

        check_type(
            value,
            str,
            optional=True,
        )

        check_type(
            errorMessage,
            str,
            optional=True,
        )

        check_type(
            isRequired,
            bool,
            optional=True,
        )

        check_type(
            label,
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
                    CARD_ELEMENTS.Image,
                    CONTAINERS.ImageSet,
                    ChoiceSet,
                    Date,
                    Number,
                    Text,
                    Time,
                    Toggle,
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
        self.id = id
        self.max = max
        self.min = min
        self.placeholder = placeholder
        self.value = value
        self.errorMessage = errorMessage
        self.isRequired = isRequired
        self.label = label
        self.fallback = fallback
        self.height = height
        self.separator = separator
        self.spacing = spacing
        self.isVisible = isVisible
        self.requires = requires

        super().__init__(
            serializable_properties=[
                *(["fallback"] if hasattr(fallback, "to_dict") else []),
            ],
            simple_properties=[
                "id",
                "type",
                "max",
                "min",
                "placeholder",
                "value",
                "errorMessage",
                "isRequired",
                "label",
                *([] if hasattr(fallback, "to_dict") else ["fallback"]),
                "height",
                "separator",
                "spacing",
                "isVisible",
                "requires",
            ],
        )


class Toggle(AdaptiveCardComponent):
    """
    **Adaptive Card - Input.Toggle Element**

    Lets a user choose between two options.
    """

    type = "Input.Toggle"

    def __init__(
        self,
        title: str,
        id: str,
        value: str = "false",
        valueOff: str = "false",
        valueOn: str = "true",
        wrap: bool = None,
        errorMessage: str = None,
        isRequired: bool = None,
        label: str = None,
        fallback: object = None,
        height: OPTIONS.BlockElementHeight = None,
        separator: bool = None,
        spacing: OPTIONS.Spacing = None,
        isVisible: bool = True,
        requires: dict[str, str] = None,
    ):
        """
        Initialize a new Input.Toggle element.

        Args:
            title (str, Mandatory): Title for the toggle.
            id (str, Mandatory): Unique identifier for the value. Used to
                identify collected input when the Submit action is performed.
            value (str, Optional): The initial selected value. If you want the
                toggle to be initially on, set this to the value of valueOn's
                value. **_Defaults to false_.**
            valueOff (str, Optional): The value when toggle is off.
                **_Defaults to false_.**
            valueOn (str, Optional): The value when toggle is on. **_Defaults
                to true_.**
            wrap (bool, Optional): If true, allow text to wrap. Otherwise,
                text is clipped. **_Defaults to None_.**
            errorMessage (str, Optional): Error message to display when
                entered input is invalid. **_Defaults to None_.**
            isRequired (bool, Optional): Whether or not this input is required.
                **_Defaults to None_.**
            label (str, Optional): Label for this input. **_Defaults to
                None_.**
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
            title,
            str,
        )

        check_type(
            id,
            str,
        )

        check_type(
            value,
            str,
            optional=True,
        )

        check_type(
            valueOff,
            str,
            optional=True,
        )

        check_type(
            valueOn,
            str,
            optional=True,
        )

        check_type(
            wrap,
            bool,
            optional=True,
        )

        check_type(
            errorMessage,
            str,
            optional=True,
        )

        check_type(
            isRequired,
            bool,
            optional=True,
        )

        check_type(
            label,
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
                    CARD_ELEMENTS.Image,
                    CONTAINERS.ImageSet,
                    ChoiceSet,
                    Date,
                    Number,
                    Text,
                    Time,
                    Toggle,
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
        self.title = title
        self.id = id
        self.value = value
        self.valueOff = valueOff
        self.valueOn = valueOn
        self.wrap = wrap
        self.errorMessage = errorMessage
        self.isRequired = isRequired
        self.label = label
        self.fallback = fallback
        self.height = height
        self.separator = separator
        self.spacing = spacing
        self.isVisible = isVisible
        self.requires = requires

        super().__init__(
            serializable_properties=[
                *(["fallback"] if hasattr(fallback, "to_dict") else []),
            ],
            simple_properties=[
                "type",
                "id",
                "title",
                "value",
                "valueOff",
                "valueOn",
                "wrap",
                "errorMessage",
                "isRequired",
                "label",
                *([] if hasattr(fallback, "to_dict") else ["fallback"]),
                "height",
                "separator",
                "spacing",
                "isVisible",
                "requires",
            ],
        )


class ChoiceSet(AdaptiveCardComponent):
    """
    **Adaptive Card - Input.ChoiceSet Element**

    Allows a user to input a Choice.
    """

    type = "Input.ChoiceSet"

    def __init__(
        self,
        id: str,
        choices: list[object] = None,
        isMultiSelect: bool = None,
        style: OPTIONS.ChoiceInputStyle = None,
        value: str = None,
        placeholder: str = None,
        wrap: bool = None,
        errorMessage: str = None,
        isRequired: bool = None,
        label: str = None,
        fallback: object = None,
        height: OPTIONS.BlockElementHeight = None,
        separator: bool = None,
        spacing: OPTIONS.Spacing = None,
        isVisible: bool = True,
        requires: dict[str, str] = None,
    ):
        """
        Initialize a new Input.ChoiceSet element.

        Args:
            id (str, Mandatory): Unique identifier for the value. Used to
                identify collected input when the Submit action is performed.
            choices (list of Choice Element(s), Optional): Choice options.
                **_Defaults to None_** Allowed value(s):
                Choice
            isMtuliSelect (bool, Optional): Allow multiple choices to be
                selected. **_Defaults to None._**
            style (ChoiceInputStyle, Optional): Style hint for choiceset input.
                **_Defaults to None_** Allowed value(s):
                ChoiceInputStyle.COMPACT or ChoiceInputStyle.EXPANDED
            value (str, Optional): The initial choice (or set of choices) that
                should be selected. For multi-select, specify a
                comma-separated string of values. **_Defaults to None_.**
            placeholder (str, Optional): Description of the input desired.
                Only visible when no selection has been made, the style is
                compact and isMultiSelect is false. **_Defaults to None_.**
            wrap (bool, Optional): If true, allow text to wrap. Otherwise,
                text is clipped. **_Defaults to None_.**
            errorMessage (str, Optional): Error message to display when
                entered input is invalid. **_Defaults to None_.**
            isRequired (bool, Optional): Whether or not this input is required.
                **_Defaults to None_.**
            label (str, Optional): Label for this input. **_Defaults to
                None_.**
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
            id,
            str,
        )

        check_type(
            choices,
            Choice,
            optional=True,
            is_list=True,
        )

        check_type(
            isMultiSelect,
            bool,
            optional=True,
        )

        validate_input(
            style,
            OPTIONS.ChoiceInputStyle,
            optional=True,
        )

        check_type(
            value,
            str,
            optional=True,
        )

        check_type(
            placeholder,
            str,
            optional=True,
        )

        check_type(
            wrap,
            bool,
            optional=True,
        )

        check_type(
            errorMessage,
            str,
            optional=True,
        )

        check_type(
            isRequired,
            bool,
            optional=True,
        )

        check_type(
            label,
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
                    CARD_ELEMENTS.Image,
                    CONTAINERS.ImageSet,
                    ChoiceSet,
                    Date,
                    Number,
                    Text,
                    Time,
                    Toggle,
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
        self.id = id
        self.choices = choices
        self.isMultiSelect = isMultiSelect
        self.style = style
        self.value = value
        self.placeholder = placeholder
        self.wrap = wrap
        self.errorMessage = errorMessage
        self.isRequired = isRequired
        self.label = label
        self.fallback = fallback
        self.height = height
        self.separator = separator
        self.spacing = spacing
        self.isVisible = isVisible
        self.requires = requires

        super().__init__(
            serializable_properties=[
                "choices",
                *(["fallback"] if hasattr(fallback, "to_dict") else []),
            ],
            simple_properties=[
                "type",
                "id",
                "isMultiSelect",
                "style",
                "value",
                "placeholder",
                "wrap",
                "errorMessage",
                "isRequired",
                "label",
                *([] if hasattr(fallback, "to_dict") else ["fallback"]),
                "height",
                "separator",
                "spacing",
                "isVisible",
                "requires",
            ],
        )


class Choice(AdaptiveCardComponent):
    """
    **Adaptive Card Choice Component**

    Describes a choice for use in a ChoiceSet.
    """

    def __init__(
        self,
        title: str,
        value: str,
    ):
        """
        Initialize a new Input.Choice element for the Input.ChoiceSet
        element.

        Args:
            title (str, Mandatory): Text to display.
            value (str, Mandatory): The raw value for the choice.
                NOTE: do not use a , in the value, since a ChoiceSet with
                isMultiSelect set to true returns a comma-delimited string of
                choice values.
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
