.. _Cards:

=================
Cards and Buttons
=================

Webex supports `AdaptiveCards <https://www.adaptivecards.io/>`_ to allow
new levels of interactivity for bots and integrations. You can read more about
how cards and buttons work `in the official guide <https://developer.webex.com/docs/api/guides/cards>`_.

In this guide we want to cover the abstraction built into the webexpythonsdk that
lets you author adaptive cards in pure python without having to touch the
underlying JSON of an adaptive card.

Sending a card
==============

Lets dive into a simple example that sends a card to a room

.. code-block:: python

    from webexpythonsdk import WebexAPI
    from webexpythonsdk.models.cards.card import AdaptiveCard
    from webexpythonsdk.models.cards.inputs import Text, Number
    from webexpythonsdk.models.cards.card_elements import TextBlock
    from webexpythonsdk.models.cards.actions import Submit

    greeting = TextBlock("Hey hello there! I am a adaptive card")
    first_name = Text('first_name', placeholder="First Name")
    age = Number('age', placeholder="Age")

    submit = Submit(title="Send me!")

    card = AdaptiveCard(body=[greeting, first_name, age], actions=[submit])

    api = WebexAPI()
    api.messages.create(text="fallback", roomId="...", attachments=[card])

The message we send with this code then looks like this in our Webex space
client:

.. image:: ../images/cards_sample.png


Processing a card action
========================


Adaptive card interactions are treated as "attachment actions". Once user interacts
with your card and submits an action, your app will receive a webhook from Webex. You
must :ref:`setup a webhook <webhooks>` in advance with ``resource = "attachmentActions"``
and ``event = "created"``.

Webhook payload will contain a JSON:

.. code-block:: json

    {
        "resource": "attachmentActions",
        "event": "created",
        "data": {
            "id": "XYXYXY",
            "type": "submit"
        }
    }

Extract attachment action ID from ``['data']['id']`` and
use :ref:`attachment_actions.get() <attachment_actions>` to get full information
about user action and any submitted data.

.. code-block:: python

    action = api.attachment_actions.get(webhookJson['data']['id'])

    first_name = action.inputs['first_name']
    age = action.inputs['age']
