"""
...
"""
import typing as t

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, pyqtBoundSignal
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import *

from core import scrap_mechanic as sm
from core.ui.page_manager_class import PageManager
from core.ui.stack_edit_ui_class import StackEditUi
from core.ui import common


class RecipeEditUi(QWidget):
    """..."""
    closed: pyqtBoundSignal = pyqtSignal()
    done: pyqtBoundSignal = pyqtSignal()

    def __init__(self, parent: QWidget = None, recipe: t.Union[sm.CraftbotRecipe, sm.DressbotRecipe, sm.RefineryRecipe] = None, restrictions: int = 0):
        QWidget.__init__(self, parent)
        uic.loadUi('core\\ui\\layout\\SMERecipeEdit.ui', self)
        self.__restrictions = restrictions
        self.__original = recipe
        self.__recipe = recipe.copy()

        self.__has_craft_time = hasattr(self.__recipe, 'craft_time')
        self.__has_reward = hasattr(self.__recipe, 'reward')
        self.__one_ingredient = hasattr(self.__recipe, 'ingredient')

        self._setupUi()
        self._bindSignals()
        self.show()

    def _setupUi(self):

        # ITEM VIEW ########################

        self._updateResultView()
        if self.__restrictions & sm.CraftbotRestrictions.NO_RESULT_EDITING:
            self.EditItemToolButton.setDisabled(True)

        # REWARD ###########################

        self.RewardComboBox: QComboBox
        if self.__has_reward:
            for name, tier in sm.DRESSBOT_REWARD_TIERS.items():
                self.RewardComboBox.addItem(name, tier)

        self.RewardFrame: QFrame
        if not self.__has_reward:
            self.RewardFrame.hide()

        # CRAFTING TIME ####################

        self.CraftingTimeSpinBox: QSpinBox
        self.CraftingTimeSpinBox.setMinimum(0)
        self.CraftingTimeSpinBox.setMaximum(300)

        if self.__has_craft_time:
            self.CraftingTimeSpinBox.setValue(self.__recipe.craft_time)

        self.CraftingTimeFrame: QFrame
        if not self.__has_craft_time:
            self.CraftingTimeFrame.hide()

        # INGREDIENTS ######################

        self.AddIngredientToolButton: QPushButton
        self.RemoveIngredientToolButton: QPushButton
        if self.__restrictions & sm.CraftbotRestrictions.NO_INGREDIENT_ADDITION:
            self.AddIngredientToolButton.hide()
            self.RemoveIngredientToolButton.hide()

        self.EditIngredientToolButton: QPushButton
        if self.__restrictions & sm.CraftbotRestrictions.NO_INGREDIENT_EDITING:
            self.EditIngredientToolButton.hide()

        self.IngredientList: QListWidget
        if self.__restrictions & sm.CraftbotRestrictions.NO_INGREDIENT_EDITING:
            self.IngredientList.setSelectionMode(QAbstractItemView.NoSelection)
            self.IngredientList.setDisabled(True)

        self._updateIngredients()

    def _bindSignals(self):
        self.EditItemToolButton: QToolButton
        self.EditItemToolButton.clicked.connect(self._EditItemToolButton_clicked)

        self.RewardComboBox: QComboBox
        self.RewardComboBox.currentIndexChanged.connect(self._RewardComboBox_currentIndexChanged)

        self.CraftingTimeSpinBox: QSpinBox
        self.CraftingTimeSpinBox.valueChanged.connect(self._CraftingTimeSpinBox_valueChanged)

        self.AddIngredientToolButton: QToolButton
        self.AddIngredientToolButton.clicked.connect(self._AddIngredientToolButton_clicked)

        self.RemoveIngredientToolButton: QToolButton
        self.RemoveIngredientToolButton.clicked.connect(self._RemoveIngredientToolButton_clicked)

        self.EditIngredientToolButton: QToolButton
        self.EditIngredientToolButton.clicked.connect(self._EditIngredientToolButton_clicked)

        self.IngredientList: QListWidget
        self.IngredientList.itemDoubleClicked.connect(self._IngredientList_itemDoubleClicked)

        self.BackButton: QPushButton
        self.BackButton.clicked.connect(self._closePage)

        self.DoneButton: QPushButton
        self.DoneButton.clicked.connect(self._doneEditing)

    def _closePage(self):
        PageManager.closeCurrentPage()
        self.closed.emit()

    def _doneEditing(self):
        self._saveChanges()
        PageManager.closeCurrentPage()
        self.done.emit()

    # WIDGET'S HELPER METHODS ###############################

    def _saveChanges(self):
        self.__recipe.copy_to(self.__original)

    def _updateResultView(self):
        result_icon: QPixmap = common.get_item_icon(self.__recipe.result.item.uuid)

        self.EditItemToolButton: QToolButton
        self.EditItemToolButton.setIcon(QIcon(result_icon.scaledToWidth(192)))

        self.ItemNameLabel: QLabel
        self.ItemNameLabel.setText(f'{self.__recipe.result.item.name} (x{self.__recipe.result.quantity})')

    def _updateIngredients(self):
        self.IngredientList: QListWidget
        self.IngredientList.clear()

        ingredients = []
        if hasattr(self.__recipe, 'ingredients'):
            ingredients = self.__recipe.ingredients
        elif hasattr(self.__recipe, 'ingredient'):
            ingredients = [sm.ItemStack(self.__recipe.ingredient, 1)]

        for ingredient in ingredients:
            item = QListWidgetItem(f'{ingredient.item.name} (x{ingredient.quantity})')

            pixmap = common.get_item_icon(ingredient.item.uuid)
            item.setIcon(QIcon(pixmap))

            item.setData(QListWidgetItem.UserType, ingredient)

            self.IngredientList.addItem(item)

    # WIDGET'S EVENT SLOTS ##################################

    def _EditItemToolButton_clicked(self):
        if self.__restrictions & sm.CraftbotRestrictions.NO_RESULT_EDITING:
            return

        page: StackEditUi = PageManager.openNewPage(StackEditUi, stack=self.__recipe.result, restrictions=self.__restrictions)
        page.done.connect(self._updateResultView)

    def _RewardComboBox_currentIndexChanged(self, index: int):
        if not self.__has_reward:
            return

        self.RewardComboBox: QComboBox
        self.__recipe.reward = self.RewardComboBox.itemData(index)

    def _CraftingTimeSpinBox_valueChanged(self, value: int):
        if not self.__has_craft_time:
            return

        self.__recipe.craft_time = value

    def _AddIngredientToolButton_clicked(self):
        if self.__one_ingredient:
            return

        stack = sm.ItemStack.default()
        self.__recipe.ingredients.insert(0, stack)

        self.IngredientList: QListWidget
        pixmap = common.get_item_icon(stack.item.uuid)
        lw_item = common.create_QListWidgetItem(stack, text=f'{stack.item.name} (x{stack.quantity})', pixmap=pixmap)
        self.IngredientList.insertItem(0, lw_item)

        page: StackEditUi = PageManager.openNewPage(StackEditUi, stack=stack, restrictions=self.__restrictions)
        page.done.connect(self._updateIngredients)

    def _RemoveIngredientToolButton_clicked(self):
        self.IngredientList: QListWidget
        if self.__one_ingredient or len(self.IngredientList.selectedItems()) == 0:
            return

        stack = self.IngredientList.selectedItems()[0].data(QListWidgetItem.UserType)
        self.__recipe.ingredients.remove(stack)
        self._updateIngredients()

    def _EditIngredientToolButton_clicked(self):
        self.IngredientList: QListWidget
        if self.__one_ingredient or len(self.IngredientList.selectedItems()) == 0:
            return

        stack = self.IngredientList.selectedItems()[0].data(QListWidgetItem.UserType)
        page: StackEditUi = PageManager.openNewPage(StackEditUi, stack=stack)
        page.done.connect(self._updateIngredients)

    def _IngredientList_itemDoubleClicked(self, item: QListWidgetItem):
        if self.__one_ingredient:
            return

        stack = item.data(QListWidgetItem.UserType)
        page: StackEditUi = PageManager.openNewPage(StackEditUi, stack=stack)
        page.done.connect(self._updateIngredients)
