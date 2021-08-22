"""
...
"""
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, pyqtBoundSignal
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import *

from core import scrap_mechanic as sm
from core.ui.page_manager_class import PageManager
from core.ui.recipe_edit_ui_class import RecipeEditUi
from core.ui import common


class RecipeListUi(QWidget):
    """..."""
    closed: pyqtBoundSignal = pyqtSignal()

    def __init__(self, parent: QWidget = None, craftbot: sm.Craftbot = None):
        QWidget.__init__(self, parent)
        uic.loadUi('core\\ui\\layout\\SMERecipeList.ui', self)
        self.__craftbot = craftbot

        self._setupUi()
        self._bindSignals()
        self.show()

    def _setupUi(self):
        self.CraftbotNameLabel: QLabel
        self.CraftbotNameLabel.setText(self.__craftbot.name)

        self.CraftbotIconLabel: QLabel
        pixmap: QPixmap = common.get_item_icon(self.__craftbot.uuid)
        self.CraftbotIconLabel.setPixmap(pixmap.scaledToWidth(48))

        self.RemoveRecipeToolButton: QToolButton
        self.AddRecipeToolButton: QToolButton
        if sm.CraftbotRestrictions.NO_RECIPE_ADDITION & self.__craftbot.restrictions:
            self.RemoveRecipeToolButton.hide()
            self.AddRecipeToolButton.hide()

        self._updateRecipeList()

    def _bindSignals(self):
        self.BackButton: QPushButton
        self.BackButton.clicked.connect(self._closePage)

        self.SearchBarLineEdit: QLineEdit
        self.SearchBarLineEdit.textChanged.connect(self._updateRecipeList)

        self.AddRecipeToolButton: QToolButton
        self.AddRecipeToolButton.clicked.connect(self._AddRecipeToolButton_clicked)

        self.RemoveRecipeToolButton: QToolButton
        self.RemoveRecipeToolButton.clicked.connect(self._RemoveRecipeToolButton_clicked)

        self.RecipeList: QListWidget
        self.RecipeList.itemDoubleClicked.connect(self._RecipeList_itemDoubleClicked)

    def _closePage(self):
        PageManager.closeCurrentPage()
        self.closed.emit()

    def _updateRecipeList(self):
        self.SearchBarLineEdit: QLineEdit
        search = self.SearchBarLineEdit.text().lower()

        items = common.search(search, sm.craft_editor.recipes[self.__craftbot], key=lambda r: r.result.item.name)

        self.RecipeList: QListWidget
        self.RecipeList.clear()
        for recipe in items:
            pixmap = common.get_item_icon(recipe.result.item.uuid)
            item = common.create_QListWidgetItem(recipe, text=recipe.result.item.name, pixmap=pixmap)
            self.RecipeList.addItem(item)

    # WIDGET'S EVENT SLOTS ##################################

    def _AddRecipeToolButton_clicked(self):
        if self.__craftbot.restrictions & sm.CraftbotRestrictions.NO_RECIPE_ADDITION:
            return

        recipe = self.__craftbot.recipe_class.default()
        sm.craft_editor.recipes[self.__craftbot].insert(0, recipe)

        self.RecipeList: QListWidget
        pixmap = common.get_item_icon(recipe.result.item.uuid)
        item = common.create_QListWidgetItem(recipe, text=recipe.result.item.name, pixmap=pixmap)
        self.RecipeList.insertItem(0, item)

        page: RecipeEditUi = PageManager.openNewPage(RecipeEditUi, recipe=recipe, restrictions=self.__craftbot.restrictions)
        page.done.connect(self._updateRecipeList)

    def _RemoveRecipeToolButton_clicked(self):
        if self.__craftbot.restrictions & sm.CraftbotRestrictions.NO_RECIPE_ADDITION:
            return

        self.RecipeList: QListWidget
        if len(self.RecipeList.selectedItems()) == 0 or QMessageBox.question(
                    self,
                    'Remove?',
                    'Recipe will be removed, there is no way to undo this operation\nDo you want to remove it anyway?',
                    QMessageBox.No | QMessageBox.Yes,
                    QMessageBox.No
                ) == QMessageBox.No:
            return

        for item in self.RecipeList.selectedItems():
            sm.craft_editor.recipes[self.__craftbot].remove(item.data(QListWidgetItem.UserType))
            self.RecipeList.removeItemWidget(item)

        self._updateRecipeList()

    def _RecipeList_itemDoubleClicked(self):
        self.RecipeList: QListWidget
        if len(self.RecipeList.selectedItems()) == 0:
            return

        recipe = self.RecipeList.selectedItems()[0].data(QListWidgetItem.UserType)
        page: RecipeEditUi = PageManager.openNewPage(RecipeEditUi, recipe=recipe, restrictions=self.__craftbot.restrictions)
        page.done.connect(self._updateRecipeList)
