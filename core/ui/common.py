"""
...
"""
import typing as t

from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QListWidget, QListWidgetItem


def get_item_icon(uuid: str):
    """Returns item's icon from ItemIconsSet0/ItemIcons and ItemIconsSurvival"""
    import core.scrap_mechanic as sm
    return sm.resource_loader.get('ItemIconsSetSurvival0/ItemIconsSurvival').get(uuid) or \
        sm.resource_loader.get('ItemIconsSet0/ItemIcons').get(uuid)


def search(val: str, lst: list, key: t.Callable[[t.Any], str] = str):
    """..."""
    items = lst
    if not val.isspace():
        starts = []
        contains = []
        for item, k in zip(lst, map(key, lst)):
            if k.startswith(val):
                starts.append(item)
            elif val in k:
                contains.append(item)
        items = starts + contains
    return items


def create_QListWidgetItem(item: t.Any, text: str = None, pixmap: QPixmap = None):
    """..."""
    lw_item = QListWidgetItem()
    lw_item.setData(QListWidgetItem.UserType, item)
    lw_item.setText(text or str(item))
    lw_item.setIcon(QIcon(pixmap))
    return lw_item
