from .abstract_components import Serializable

class OpenUrl(Serializable):
    def __init__(self, url, title=None,
                            iconURL=None):
        self.type = "Action.OpenUrl"
        self.title = title
        self.iconURL = iconURL

        super().__init__(serializable_properties=[],
                         simple_properties=['type', 'title', 'iconURL'])

class Submit(Serializable):
    def __init__(self, data=None,
                       title=None,
                       iconURL=None,
                       ):
        self.type = "Action.Submit"
        self.data = data
        self.title = title
        self.iconURL = iconURL

        super().__init__(serializable_properties=['data'],
                         simple_properties=['title', 'iconURL', 'type'])

class ShowCard(Serializable):
    def __init__(self, card=None,
                       title=None,
                       iconURL=None):
        self.type = "Action.ShowCard"
        self.card = card
        self.title = title
        self.iconURL = iconURL

        super().__init__(serializable_properties=['card'],
                         simple_properties=['title', 'type', 'iconURL'])
