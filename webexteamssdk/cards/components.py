from .abstract_components import Serializable

class MediaSource(Serializable):
    def __init__(self,
                 mimeType,
                 url):
        self.mimeType = mimeType
        self.url = url

        super().__init__(serializable_properties=[],
                         simple_properties=['mimeType', 'url'])

class Media(Serializable):
    def __init__(self,
                 sources,
                 poster=None,
                 altText=None,
                 height=None,
                 separator=None,
                 spacing=None,
                 id=None):
        self.type = "Media"
        self.sources = sources #Needs to be a list of media sources
        self.poster = poster
        self.altText = altText
        self.height = height
        self.separator = separator
        self.spacing = spacing
        self.id = id

        super().__init__(serializable_properties=['sources'],
                         simple_properties=[
                            'type', 'poster', 'altText', 'height',
                            'separator', 'spacing', 'id'
                         ])
class Image(Serializable):
    def __init__(self,
                 url,
                 altText=None,
                 backgroundColor=None,
                 height=None,
                 horizontalAlignment=None,
                 selectAction=None,
                 size=None,
                 style=None,
                 width=None,
                 seperator=None,
                 spacing=None,
                 id=None):

        self.type = "Image"
        self.url = url
        self.altText = altText
        self.backgroundColor = backgroundColor
        self.height = height
        self.horizontalAlignment = horizontalAlignment
        self.selectAction = selectAction
        self.size = size
        self.style = style
        self.width = width
        self.seperator = seperator
        self.spacing = spacing
        self.id = id

        super().__init__(serializable_properties=[],
                         simple_properties=[
                            'type', 'url', 'altText', 'backgroundColor',
                            'height', 'horizontalAlignment', 'selectAction',
                            'size', 'style', 'width', 'separator', 'spacing',
                            'id'
                         ])
class TextBlock(Serializable):
    def __init__(self,
                 text,
                 color=None,
                 horizontalAlignment=None,
                 isSubtle=None,
                 maxLines=None,
                 size=None,
                 weight=None,
                 wrap=None,
                 separator=None,
                 spacing=None,
                 id=None):


        #ToDo(mneiding): Type check
        self.type = "TextBlock"
        self.text = text
        self.color = color
        self.horizontalAlignment = horizontalAlignment
        self.isSubtle = isSubtle
        self.maxLines = maxLines
        self.size = size
        self.weight = weight
        self.wrap = wrap
        self.separator = separator
        self.spacing = spacing
        self.id = id

        super().__init__(serializable_properties=[],
                         simple_properties=[
                            'type', 'text', 'color', 'horizontalAlignment',
                            'isSubtle', 'maxLines', 'size', 'weight', 'wrap',
                            'spacing', 'id', 'separator'
                        ])
class Column(Serializable):
    def __init__(self, items=None,
                       separator=None,
                       spacing=None,
                       selectAction=None,
                       style=None,
                       verticalContentAlignment=None,
                       width=None,
                       id=None):
        self.type = "Column"
        self.items = items
        self.separator = separator
        self.spacing = spacing
        self.selectAction = selectAction
        self.style = style
        self.verticalContentAlignment = verticalContentAlignment
        self.width = width
        self.id = id

        super().__init__(serializable_properties=['items'],
                         simple_properties=[
                            'type', 'separator', 'spacing', 'selectAction',
                            'style', 'verticalContentAlignment', 'width', 'id'
                         ])

class Fact(Serializable):
    def __init__(self, title, value):
        self.title = title
        self.value = value

        super().__init__(serializable_properties=[],
                         simple_properties=['title', 'value'])

class Choice(Serializable):
    def __init__(self, title, value):
        self.title = title
        self.value = value

        super().__init__(serializable_properties=[],
                         simple_properties=['title', 'value'])
