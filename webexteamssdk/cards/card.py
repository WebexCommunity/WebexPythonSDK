from .abstract_components import Serializable, Component

class AdaptiveCard(Serializable):
    def __init__(self, body=None,
                       actions=None,
                       selectAction=None,
                       style=None,
                       fallbackText=None,
                       lang=None):
        super().__init__(serializable_properties=['body', 'actions', 'selectAction', 'style'],
                         simple_properties=['version', 'fallbackText', 'lang', 'schema', 'type'])

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
