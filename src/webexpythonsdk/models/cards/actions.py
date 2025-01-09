"""Webex Adaptive Card - Actions Model.

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
import webexpythonsdk.models.cards.cards as CARDS
import webexpythonsdk.models.cards.options as OPTIONS
from webexpythonsdk.models.cards.utils import (
    check_type,
    validate_input,
    validate_dict_str,
    validate_uri,
)


class OpenUrl(AdaptiveCardComponent):
    """
    **Adaptive Card - Action.OpenUrl Element**

    When invoked, show the given url either by launching it in an external web
    browser or showing within an embedded web browser.
    """

    type = "Action.OpenUrl"

    def __init__(
        self,
        url: object,
        title: str = None,
        iconUrl: object = None,
        id: str = None,
        style: OPTIONS.ActionStyle = None,
        fallback: object = None,
        requires: dict[str, str] = None,
    ):
        """
        Initialize a new Action.OpenUrl element.

        Args:
            url (uri, Mandatory): The URL to open. Allowed value(s):
                uri
            title (str, Optional): Label for button or link that represents
                this action.  **_Defaults to None._**
            iconUrl (uri, Optional): Optional icon to be shown on the action
                in conjunction with the title. Supports data URI. **_Defaults
                to None._** Allowed value(s):
                uri
            id (str, Optional): A unique identifier associated with this
                Action. **_Defaults to None._**
            style (ActionStyle, Optional): Controls the style of an Action,
                which influences how the action is displayed, spoken, etc.
                **_Defaults to None._** Allowed
                value(s):
                ActionStyle.DEFAULT, ActionStyle.POSITIVE, or
                ActionStyle.DESTRUCTIVE
            fallback (Action Element or str, Optional): Describes what to do
                when an unknown element is encountered or the requires of this
                or any children can't be met. **_Defaults to None._** Allowed
                value(s):
                OpenUrl, ShowCard, Submit, ToggleVisibility, or "drop".
                Note: "drop" causes this element to be dropped immediately
                when unknown elements are encountered. The unknown element
                doesn't bubble up any higher.
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
            title,
            str,
            optional=True,
        )

        validate_uri(
            iconUrl,
            optional=True,
        )

        check_type(
            id,
            str,
            optional=True,
        )

        validate_input(
            style,
            OPTIONS.ActionStyle,
            optional=True,
        )

        if hasattr(fallback, "to_dict"):
            check_type(
                fallback,
                (
                    OpenUrl,
                    ShowCard,
                    Submit,
                    ToggleVisibility,
                ),
                optional=True,
            )
        else:
            validate_input(
                fallback,
                "drop",
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
        self.title = title
        self.iconUrl = iconUrl
        self.id = id
        self.style = style
        self.fallback = fallback
        self.requires = requires

        super().__init__(
            serializable_properties=[
                *(["fallback"] if hasattr(fallback, "to_dict") else []),
            ],
            simple_properties=[
                "type",
                "url",
                "title",
                "iconUrl",
                "id",
                "style",
                *([] if hasattr(fallback, "to_dict") else ["fallback"]),
                "requires",
            ],
        )


class Submit(AdaptiveCardComponent):
    """
    **Adaptive Card - Action.Submit Element**

    Gathers input fields, merges with optional data field, and sends an event
    to the client. It is up to the client to determine how this data is
    processed. For example: With BotFramework bots, the client would send an
    activity through the messaging medium to the bot. The inputs that are
    gathered are those on the current card, and in the case of a show card
    those on any parent cards. See
    https://docs.microsoft.com/en-us/adaptive-cards/authoring-cards/input-validation
    for more details.
    """

    type = "Action.Submit"

    def __init__(
        self,
        data: object = None,
        associatedInputs: OPTIONS.AssociatedInputs = OPTIONS.AssociatedInputs.AUTO,
        title: str = None,
        iconUrl: object = None,
        id: str = None,
        style: OPTIONS.ActionStyle = None,
        fallback: object = None,
        requires: dict[str, str] = None,
    ):
        """
        Initialize a new Action.Submit element.

        Args:
            data (str or object, Optional): Initial data that input fields
                will be combined with. These are essentially "hidden"
                properties. **_Defaults to None._** Allowed value(s):
                str or object
            associatedInputs (AssociatedInputs, Optional): Controls which
                inputs are associated with the submit action. **_Defaults to
                AssociatedInputs.AUTO_.** Allowed value(s):
                AssociatedInputs.AUTO or AssociatedInputs.NONE
            title (str, Optional): Label for button or link that represents
                this action. **_Defaults to None._**
            iconUrl (uri, Optional): Optional icon to be shown on the action
                in conjunction with the title. Supports data URI. **_Defaults
                to None._** Allowed value(s):
                uri
            id (str, Optional): A unique identifier associated with this
                Action. **_Defaults to None._**
            style (ActionStyle, Optional): Controls the style of an Action,
                which influences how the action is displayed, spoken, etc.
                **_Defaults to None._** Allowed value(s):
                ActionStyle.DEFAULT, ActionStyle.POSITIVE, or
                ActionStyle.DESTRUCTIVE
            fallback (Action Element or str, Optional): Describes what to do
                when an unknown element is encountered or the requires of this
                or any children can't be met. **_Defaults to None._** Allowed
                value(s):
                OpenUrl, ShowCard, Submit, ToggleVisibility, or "drop".
                Note: "drop" causes this element to be dropped immediately
                when unknown elements are encountered. The unknown element
                doesn't bubble up any higher.
            requires (Dictionary(string), Optional): A series of key/value
                pairs indicating features that the item requires with
                corresponding minimum version. When a feature is missing or of
                insufficient version, fallback is triggered. In the Dictionary,
                both key(s) and value(s) should be of str datatype. **_Defaults
                to None._**
        """
        # Check types
        check_type(
            data,
            (
                str,
                object,
            ),
            optional=True,
        )

        validate_input(
            associatedInputs,
            OPTIONS.AssociatedInputs,
            optional=True,
        )

        check_type(
            title,
            str,
            optional=True,
        )

        validate_uri(
            iconUrl,
            optional=True,
        )

        check_type(
            id,
            str,
            optional=True,
        )

        validate_input(
            style,
            OPTIONS.ActionStyle,
            optional=True,
        )

        if hasattr(fallback, "to_dict"):
            check_type(
                fallback,
                (
                    OpenUrl,
                    ShowCard,
                    Submit,
                    ToggleVisibility,
                ),
                optional=True,
            )
        else:
            validate_input(
                fallback,
                "drop",
                optional=True,
            )

        validate_dict_str(
            requires,
            str,
            str,
            optional=True,
        )

        # Set properties
        self.data = data
        self.associatedInputs = associatedInputs
        self.title = title
        self.iconUrl = iconUrl
        self.id = id
        self.style = style
        self.fallback = fallback
        self.requires = requires

        super().__init__(
            serializable_properties=[
                *(["fallback"] if hasattr(fallback, "to_dict") else []),
            ],
            simple_properties=[
                "type",
                "data",
                "associatedInputs",
                "title",
                "iconUrl",
                "id",
                "style",
                *([] if hasattr(fallback, "to_dict") else ["fallback"]),
                "requires",
            ],
        )


class ShowCard(AdaptiveCardComponent):
    """
    **Adaptive Card - Action.ShowCard Element**

    Defines an AdaptiveCard which is shown to the user when the button or link
    is clicked.
    """

    type = "Action.ShowCard"

    def __init__(
        self,
        card: object = None,
        title: str = None,
        iconUrl: object = None,
        id: str = None,
        style: OPTIONS.ActionStyle = None,
        fallback: object = None,
        requires: dict[str, str] = None,
    ):
        """
        Initialize a new Action.ShowCard element.

        Args:
            card (AdaptiveCard, Optional): The Adaptive Card to show. Inputs
                in ShowCards will not be submitted if the submit button is
                located on a parent card. See
                https://docs.microsoft.com/en-us/adaptive-cards/authoring-cards/input-validation
                for more details. **_Defaults to None._** Allowed value(s):
                AdaptiveCard
            title (str, Optional): Label for button or link that represents
                this action. **_Defaults to None._**
            iconUrl (uri, Optional): Optional icon to be shown on the action
                in conjunction with the title. Supports data URI. **_Defaults
                to None._** Allowed value(s):
                uri
            id (str, Optional): A unique identifier associated with this
                Action. **_Defaults to None._**
            style (ActionStyle, Optional): Controls the style of an Action,
                which influences how the action is displayed, spoken, etc.
                **_Defaults to None._** Allowed
                value(s):
                ActionStyle.DEFAULT, ActionStyle.POSITIVE, or
                ActionStyle.DESTRUCTIVE
            fallback (Action Element or str, Optional): Describes what to do
                when an unknown element is encountered or the requires of this
                or any children can't be met. **_Defaults to None._** Allowed
                value(s):
                OpenUrl, ShowCard, Submit, ToggleVisibility, or "drop".
                Note: "drop" causes this element to be dropped immediately
                when unknown elements are encountered. The unknown element
                doesn't bubble up any higher.
            requires (Dictionary(string), Optional): A series of key/value
                pairs indicating features that the item requires with
                corresponding minimum version. When a feature is missing or of
                insufficient version, fallback is triggered. In the Dictionary,
                both key(s) and value(s) should be of str datatype. **_Defaults
                to None._**
        """
        # Check types
        check_type(
            card,
            CARDS.AdaptiveCard,
            optional=True,
        )

        check_type(
            title,
            str,
            optional=True,
        )

        validate_uri(
            iconUrl,
            optional=True,
        )

        check_type(
            id,
            str,
            optional=True,
        )

        validate_input(
            style,
            OPTIONS.ActionStyle,
            optional=True,
        )

        if hasattr(fallback, "to_dict"):
            check_type(
                fallback,
                (
                    OpenUrl,
                    ShowCard,
                    Submit,
                    ToggleVisibility,
                ),
                optional=True,
            )
        else:
            validate_input(
                fallback,
                "drop",
                optional=True,
            )

        validate_dict_str(
            requires,
            str,
            str,
            optional=True,
        )

        # Set properties
        self.card = card
        self.title = title
        self.iconUrl = iconUrl
        self.id = id
        self.style = style
        self.fallback = fallback
        self.requires = requires

        super().__init__(
            serializable_properties=[
                "card",
                *(["fallback"] if hasattr(fallback, "to_dict") else []),
            ],
            simple_properties=[
                "type",
                "title",
                "iconUrl",
                "id",
                "style",
                *([] if hasattr(fallback, "to_dict") else ["fallback"]),
                "requires",
            ],
        )


class ToggleVisibility(AdaptiveCardComponent):
    """
    **Adaptive Card - Action.ToggleVisibility Element**

    An action that toggles the visibility of associated card elements.
    """

    type = "Action.ToggleVisibility"

    def __init__(
        self,
        targetElements: list[object],
        title: str = None,
        iconUrl: object = None,
        id: str = None,
        style: OPTIONS.ActionStyle = None,
        fallback: object = None,
        requires: dict[str, str] = None,
    ):
        """
        Initialize a new Action.ToggleVisibility element.

        Args:
            targetElements (list of TargetElement(s) or str, Mandatory): The
                array of TargetElements. It is not recommended to include
                Input elements with validation under Action.Toggle due to
                confusion that can arise from invalid inputs that are not
                currently visible. See
                https://docs.microsoft.com/en-us/adaptive-cards/authoring-cards/input-validation
                for more information. Allowed value(s):
                TargetElement or str
            title (str, Optional): Label for button or link that represents
                this action. **_Defaults to None._**
            iconUrl (uri, Optional): Optional icon to be shown on the action
                in conjunction with the title. Supports data URI. **_Defaults
                to None._** Allowed value(s):
                uri
            id (str, Optional): A unique identifier associated with this
                Action. **_Defaults to None._**
            style (ActionStyle, Optional): Controls the style of an Action,
                which influences how the action is displayed, spoken, etc.
                **_Defaults to None._** Allowed value(s):
                ActionStyle.DEFAULT, ActionStyle.POSITIVE, or
                ActionStyle.DESTRUCTIVE
            fallback (Action Element or str, Optional): Describes what to do
                when an unknown element is encountered or the requires of this
                or any children can't be met. **_Defaults to None._** Allowed
                value(s):
                OpenUrl, ShowCard, Submit, ToggleVisibility, or "drop".
                Note: "drop" causes this element to be dropped immediately
                when unknown elements are encountered. The unknown element
                doesn't bubble up any higher.
            requires (Dictionary(string), Optional): A series of key/value
                pairs indicating features that the item requires with
                corresponding minimum version. When a feature is missing or of
                insufficient version, fallback is triggered. In the Dictionary,
                both key(s) and value(s) should be of str datatype. **_Defaults
                to None._**
        """
        # Check types
        check_type(
            targetElements,
            (
                TargetElement,
                str,
            ),
            is_list=True,
        )

        check_type(
            title,
            str,
            optional=True,
        )

        validate_uri(
            iconUrl,
            optional=True,
        )

        check_type(
            id,
            str,
            optional=True,
        )

        validate_input(
            style,
            OPTIONS.ActionStyle,
            optional=True,
        )

        if hasattr(fallback, "to_dict"):
            check_type(
                fallback,
                (
                    OpenUrl,
                    ShowCard,
                    Submit,
                    ToggleVisibility,
                ),
                optional=True,
            )
        else:
            validate_input(
                fallback,
                "drop",
                optional=True,
            )

        validate_dict_str(
            requires,
            str,
            str,
            optional=True,
        )

        # Set properties
        self.targetElements = targetElements
        self.title = title
        self.iconUrl = iconUrl
        self.id = id
        self.style = style
        self.fallback = fallback
        self.requires = requires

        super().__init__(
            serializable_properties=[
                "targetElements",
                *(["fallback"] if hasattr(fallback, "to_dict") else []),
            ],
            simple_properties=[
                "type",
                "title",
                "iconUrl",
                "id",
                "style",
                *([] if hasattr(fallback, "to_dict") else ["fallback"]),
                "requires",
            ],
        )


class TargetElement(AdaptiveCardComponent):
    """
    **Adaptive Card - TargetElement Element**

    Represents an entry for Action.ToggleVisibility's targetElements property.
    """

    def __init__(
        self,
        elementId: str,
        isVisible: bool = None,
    ):
        """
        Initialize a new TargetElement element for the
        Action.ToggleVisibility element's targetElements argument.

        Args:
            elementId (str, Mandatory): Element ID of element to toggle.
            isVisible (uri, Optional): If true, always show target element. If
                false, always hide target element. If not supplied, toggle
                target element's visibility. **_Defaults to None._**
        """
        # Check types
        check_type(
            elementId,
            str,
        )

        check_type(
            isVisible,
            bool,
            optional=True,
        )

        # Set properties
        self.elementId = elementId
        self.isVisible = isVisible

        super().__init__(
            serializable_properties=[],
            simple_properties=[
                "elementId",
                "isVisible",
            ],
        )
