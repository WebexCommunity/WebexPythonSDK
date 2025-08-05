"""Webex Adaptive Card - Cards Model.

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
import webexpythonsdk.models.cards.card_elements as CARD_ELEMENTS
import webexpythonsdk.models.cards.containers as CONTAINERS
import webexpythonsdk.models.cards.actions as ACTIONS
import webexpythonsdk.models.cards.inputs as INPUTS
import webexpythonsdk.models.cards.types as TYPES
import webexpythonsdk.models.cards.options as OPTIONS
from webexpythonsdk.models.cards.utils import (
    check_type,
    validate_input,
    validate_uri,
)


class AdaptiveCard(AdaptiveCardComponent):
    """
    **Adaptive Card - Adaptive Card Element**

    An Adaptive Card, containing a free-form body of card elements, and an
    optional set of actions.

    **_Note:_** Webex currently supports version 1.3 of adaptive cards and
    thus only features from that release are supported in this abstraction.
    """

    type = "AdaptiveCard"
    schema = "http://adaptivecards.io/schemas/adaptive-card.json"
    version = "1.3"

    def __init__(
        self,
        body: list[object] = None,
        actions: list[object] = None,
        selectAction: object = None,
        fallbackText: str = None,
        backgroundImage: object = None,
        minHeight: str = None,
        speak: str = None,
        style: OPTIONS.ContainerStyle = None,
        lang: str = None,
        verticalContentAlignment: OPTIONS.VerticalContentAlignment = None,
    ):
        """
        Initialize a new Adaptive Card element.

        Args:
            body (list of Card Element(s), Optional): The card elements to
                show in the primary card region. **_Defaults to None._**
                Allowed value(s):
                ActionSet, ColumnSet, Container, FactSet, Image, ImageSet,
                ChoiceSet, Date, Number, Text, Time, Toggle, Media,
                RichTextBlock, TextBlock
            actions (list of Actions Element(s), Optional): The Actions to
                show in the card's action bar. **_Defaults to None._** Allowed
                value(s):
                OpenUrl, ShowCard, Submit, ToggleVisibility
            selectAction (Actions Element, Optional): An Action that will be
                invoked when the card is tapped or selected. Action.ShowCard
                is not supported. **_Defaults to None._** Allowed value(s):
                OpenUrl, Submit, or ToggleVisibility
            fallbackText (str, Optional): Text shown when the client doesn't
                support the version specified (may contain markdown).
                **_Defaults to None._**
            backgroundImage (BackgroundImage or uri, Optional): Specifies the
                background image of the card. **_Defaults to None._** Allowed
                value(s):
                BackgroundImage or uri
            minHeight (str, Optional): Specifies the minimum height of the
                card. **_Defaults to None._**
            speak (str, Optional): Specifies what should be spoken for this
                entire card. This is simple text or SSML fragment. **_Defaults
                to None._**
            style (ContainerStyle, Optional): Style hint for Container.
                **_Defaults to None._**Allowed value(s):
                ContainerStyle.DEFAULT, ContainerStyle.EMPHASIS,
                ContainerStyle.GOOD, ContainerStyle.ATTENTION,
                ContainerStyle.WARNING, or ContainerStyle.ACCENT
            lang (str, Optional): The 2-letter ISO-639-1 language used in the
                card. Used to localize any date/time functions. **_Defaults to
                None._**
            verticalContentAlignment (VerticalContentAlignment, Optional):
                Defines how the content should be aligned vertically within
                the container. Only relevant for fixed-height cards, or cards
                with a minHeight specified. **_Defaults to None._** Allowed
                value(s):
                VerticalContentAlignment.TOP, VerticalContentAlignment.CENTER,
                or VerticalContentAlignment.BOTTOM

        """
        # Check types
        check_type(
            body,
            (
                CONTAINERS.ActionSet,
                CONTAINERS.ColumnSet,
                CONTAINERS.Container,
                CONTAINERS.FactSet,
                CARD_ELEMENTS.Image,
                CONTAINERS.ImageSet,
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

        check_type(
            actions,
            (
                ACTIONS.OpenUrl,
                ACTIONS.ShowCard,
                ACTIONS.Submit,
                ACTIONS.ToggleVisibility,
            ),
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

        check_type(
            fallbackText,
            str,
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
                uri=backgroundImage,
                optional=True,
            )

        check_type(
            minHeight,
            str,
            optional=True,
        )

        check_type(
            speak,
            str,
            optional=True,
        )

        validate_input(
            style,
            OPTIONS.ContainerStyle,
            optional=True,
        )

        check_type(
            lang,
            str,
            optional=True,
        )

        check_type(
            verticalContentAlignment,
            str,
            optional=True,
        )

        validate_input(
            verticalContentAlignment,
            OPTIONS.VerticalContentAlignment,
            optional=True,
        )

        # Set properties
        self.body = body
        self.actions = actions
        self.selectAction = selectAction
        self.fallbackText = fallbackText
        self.backgroundImage = backgroundImage
        self.minHeight = minHeight
        self.speak = speak
        self.style = style
        self.lang = lang
        self.verticalContentAlignment = verticalContentAlignment

        super().__init__(
            serializable_properties=[
                "body",
                "actions",
                "selectAction",
                *(
                    ["backgroundImage"]
                    if hasattr(backgroundImage, "to_dict")
                    else []
                ),
            ],
            simple_properties=[
                "type",
                "version",
                "fallbackText",
                *(
                    []
                    if hasattr(backgroundImage, "to_dict")
                    else ["backgroundImage"]
                ),
                "minHeight",
                "speak",
                "style",
                "lang",
                "verticalContentAlignment",
            ],
        )

    def to_dict(self):
        # We need to overwrite the to_dict method to add the $schema
        # property that can't be specified the normal way due to the
        # `$` in the property name.
        serialized_data = super().to_dict()
        serialized_data["$schema"] = self.schema
        return serialized_data
