"""
Module for manipulating qt stylesheets
"""
import typing as t

from PyQt5.QtGui import QPixmap

style_paths = [
    'core/res/themes',
    'user/themes'
]


class StylePreview(t.NamedTuple):
    """StylePreview"""
    name: str
    authors: list[str]
    version: str
    version_number: int


def list_styles():
    """Loads info.json files for styles located in paths listed in style_paths variable"""
    pass


class Style:
    """Class that represents style of an app"""
    preview: StylePreview
    stylesheet: str
    resources: list[QPixmap]


class StyleRack:
    """Basically an object that represents a list of loaded styles"""

    def __init__(self):
        self.__rack: list[Style] = []

    def load(self):
        """Loads and adds style to a rack"""
        pass

    def get_stylesheet(self):
        """Returns overall stylesheet, the combination of stylesheets from all loaded styles"""
        pass

    def get_resource(self, name: str):
        """Tries to find resource in loaded styles, on failure returns None"""
        pass
