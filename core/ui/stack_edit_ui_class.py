"""
...
"""
import typing as t

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, pyqtBoundSignal
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import *

from core import scrap_mechanic as sm
from core.ui import common
from core.ui.page_manager_class import PageManager


class StackEditUi(QWidget):
    """..."""
    closed: pyqtBoundSignal = pyqtSignal()
    done: pyqtBoundSignal = pyqtSignal()

    def __init__(self, parent: QWidget = None, stack: sm.ItemStack = None, restrictions: sm.CraftbotRestrictions = 0):
        QWidget.__init__(self, parent)
        uic.loadUi('core\\ui\\layout\\SMEStackEdit.ui', self)
        self.__restrictions = restrictions
        self.__original = stack
        self.__stack = stack.copy()

        self._setupUi()
        self._bindSignals()
        self.show()

    def _setupUi(self):
        self._updateStackView()

        self.QuantitySpinBox: QSpinBox
        self.QuantitySpinBox.setMinimum(1)
        self.QuantitySpinBox.setMaximum(256)
        self.QuantitySpinBox.setValue(self.__stack.quantity)

        self.SearchBarLineEdit: QLineEdit
        self.SearchBarLineEdit.setFocus()

        self._updateItemList()

    def _bindSignals(self):
        self.QuantitySpinBox: QSpinBox
        self.QuantitySpinBox.valueChanged.connect(self._QuantitySpinBox_valueChanged)

        self.SearchBarLineEdit: QLineEdit
        self.SearchBarLineEdit.textChanged.connect(self._updateItemList)

        self.BackButton: QPushButton
        self.BackButton.clicked.connect(self._closePage)

        self.DoneButton: QPushButton
        self.DoneButton.clicked.connect(self._doneEditing)

        self.ItemList: QListWidget
        self.ItemList.itemClicked.connect(self._ItemList_itemClicked)
        self.ItemList.itemDoubleClicked.connect(self._doneEditing)

    def _closePage(self):
        PageManager.closeCurrentPage()
        self.closed.emit()

    def _doneEditing(self):
        self._saveChanges()
        PageManager.closeCurrentPage()
        self.done.emit()

    # WIDGET'S HELPER METHODS ###############################

    def _saveChanges(self):
        self.__stack.copy_to(self.__original)

    def _updateStackView(self):
        self.ItemIconLabel: QLabel
        pixmap = common.get_item_icon(self.__stack.item.uuid)
        self.ItemIconLabel.setPixmap(pixmap)

        self.ItemNameLabel: QLabel
        self.ItemNameLabel.setText(self.__stack.item.name)

    def _updateItemList(self):
        self.SearchBarLineEdit: QLineEdit
        search = self.SearchBarLineEdit.text().lower()

        items = common.search(search, sm.craft_editor.items, key=lambda i: i.name)

        self.ItemList: QListWidget
        self.ItemList.clear()
        for item in items:
            pixmap = common.get_item_icon(item.uuid)
            lw_item = common.create_QListWidgetItem(item, text=item.name, pixmap=pixmap)
            self.ItemList.addItem(lw_item)

    # WIDGET'S EVENT SLOTS ##################################

    def _QuantitySpinBox_valueChanged(self, value: int):
        self.__stack.quantity = value

    def _ItemList_itemClicked(self, item: QListWidgetItem):
        self.__stack.item = item.data(QListWidgetItem.UserType)
        self._updateStackView()
