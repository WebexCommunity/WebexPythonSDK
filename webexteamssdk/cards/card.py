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

class AdaptiveCard(Serializable):
    """AdaptiveCard class that represents a adaptive card python object.

    Note:
        Webex Teams currently supports version 1.1 of adaptive cards and thus
        only features from that release are supported in this abstraction.
    """
    def __init__(self, body=None,
                       actions=None,
                       selectAction=None,
                       style=None,
                       fallbackText=None,
                       lang=None):
        """Creates a new adaptive card object.

        Args:
            body(list): The list of components and containers making up the
                body of this adaptive card.
            actions(list): The list of actions this adaptive card should contain
            selectAction(action): The action that should be invoked when this
                adaptive card is selected. Can be any action other then
                'ShowCard'
            fallbackText(str): The text that should be displayed on clients that
                can't render adaptive cards
            lang(str): The 2-letter ISO-639-1 language used in the card. This is
                used for localization of date/time functions

        """
        super().__init__(serializable_properties=[
                            'body', 'actions', 'selectAction', 'style'
                         ],
                         simple_properties=[
                            'version', 'fallbackText', 'lang', 'schema', 'type'
                         ])

        # Set properties
        self.type = "AdaptiveCard"
        self.version = "1.1" # This is the version currently supported in Teams
        self.body = body
        self.actions = actions
        self.selectAction = selectAction
        self.style = style
        self.fallbackText = fallbackText
        self.lang = lang
        self.schema = "http://adaptivecards.io/schemas/adaptive-card.json"
