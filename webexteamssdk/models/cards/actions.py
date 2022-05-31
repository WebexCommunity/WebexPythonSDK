# -*- coding: utf-8 -*-
"""Webex Teams Adaptive Card actions.

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

from .adaptive_card_component import AdaptiveCardComponent


class OpenUrl(AdaptiveCardComponent):
    """Open URL Action."""
    type = "Action.OpenUrl"

    def __init__(self, url, title=None, iconURL=None):
        self.url = url
        self.title = title
        self.iconURL = iconURL

        super().__init__(
            serializable_properties=[],
            simple_properties=['url', 'type', 'title', 'iconURL'],
        )


class Submit(AdaptiveCardComponent):
    """Submit Action."""
    type = "Action.Submit"

    def __init__(self, data=None, title=None, iconURL=None):
        self.data = data
        self.title = title
        self.iconURL = iconURL

        super().__init__(
            serializable_properties=[],
            simple_properties=['data', 'title', 'iconURL', 'type'],
        )


class ShowCard(AdaptiveCardComponent):
    """Show Card Action."""
    type = "Action.ShowCard"

    def __init__(self, card=None, title=None, iconURL=None):
        self.card = card
        self.title = title
        self.iconURL = iconURL

        super().__init__(
            serializable_properties=['card'],
            simple_properties=['title', 'type', 'iconURL'],
        )
