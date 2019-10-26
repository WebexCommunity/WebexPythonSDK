from .abstract_components import Serializable

class Container(Serializable):
    def __init__(self, items, selectAction=None,
                              style=None,
                              verticalContentAlignment=None,
                              height=None,
                              separator=None,
                              spacing=None,
                              id=None):
        self.type = "Container"
        self.items = items
        self.selectAction = selectAction
        self.style = style
        self.verticalContentAlignment = verticalContentAlignment
        self.height = height
        self.separator = separator
        self.spacing = spacing
        self.id = id

        super().__init__(serializable_properties=['items'],
                         simple_properties=[
                            'selectAction', 'style', 'verticalContentAlignment',
                            'height', 'separator', 'spacing', 'id', 'type'
                         ])

class ColumnSet(Serializable):
    def __init__(self, columns=None,
                       selectAction=None,
                       height=None,
                       separator=None,
                       spacing=None,
                       id=None):
        self.type = "ColumnSet"
        self.columns = columns
        self.selectAction = selectAction
        self.height = height
        self.separator = separator
        self.spacing = spacing
        self.id = id

        super().__init__(serializable_properties=['columns'],
                         simple_properties=[
                            'selectAction', 'height', 'separator', 'spacing',
                            'id', 'type'
                         ])

class FactSet(Serializable):
    def __init__(self, facts, height=None,
                              separator=None,
                              spacing=None,
                              id=None):
        self.type = "FactSet"
        self.facts = facts
        self.height = height
        self.separator = separator
        self.spacing = spacing
        self.id = id

        super().__init__(serializable_properties=['facts'],
                         simple_properties=[
                            'type', 'height', 'separator', 'id', 'spacing'
                         ])

class ImageSet(Serializable):
    def __init__(self, images, imageSize=None,
                               height=None,
                               separator=None,
                               spacing=None,
                               id=None):
        self.type = "ImageSet"
        self.images = images
        self.imageSize = imageSize
        self.height = height
        self.separator = separator
        self.spacing = spacing
        self.id = id

        super().__init__(serializable_properties=['images'],
                         simple_properties=[
                            'imageSize', 'height', 'separator', 'spacing', 'id',
                            'type'
                        ])
