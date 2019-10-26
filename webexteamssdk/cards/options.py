from enum import Enum

class AbstractOption(Enum):
    def to_value(self):
        return str(self.name).lower()

    def __str__(self):
        return self.to_value()

    def __repr__(self):
        return self.to_value()

class Colors(AbstractOption):
    DEFAULT = 1
    DARK = 2
    LIGHT = 3
    ACCENT = 4
    GOOD = 5
    WARNING = 6
    ATTENTION = 7

class HorizontalAlignment(AbstractOption):
    LEFT = 1
    CENTER = 2
    RIGHT = 3

class FontSize(AbstractOption):
    DEFAULT = 1
    SMALL = 2
    MEDIUM = 3
    LARGE = 4
    EXTRALARGE = 5

class FontWeight(AbstractOption):
    DEFAULT = 1
    LIGHTER = 2
    BOLDER = 3

class BlockElementHeight(AbstractOption):
    AUTO = 1
    STRETCH = 2

class Spacing(AbstractOption):
    DEFAULT = 1
    NONE = 2
    SMALL = 3
    MEDIUM = 4
    LARGE = 5
    EXTRALARGE = 6
    PADDING = 7
