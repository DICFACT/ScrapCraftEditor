"""
...
"""
import os

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, pyqtBoundSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

from core.project import Project
from core.ui import common
from core.ui.page_manager_class import PageManager

from core import scrap_mechanic as sm, gls
from core.ui.recipe_list_ui_class import RecipeListUi


class ProjectHomeUi(QWidget):
    """..."""
    closed: pyqtBoundSignal = pyqtSignal()

    def __init__(self, parent: QWidget = None):
        QWidget.__init__(self, parent)
        uic.loadUi('core\\ui\\layout\\SMEProjectHome.ui', self)

        self._setupUi()
        self._bindSignals()
        self.show()

    def _setupUi(self):
        self.ProjectNameLabel: QLabel
        self.ProjectNameLabel.setText(Project.name)

        self.ProjectAuthorLabel: QLabel
        self.ProjectAuthorLabel.setText(f'by {Project.author}')

        self.ProjectFrame: QFrame
        if Project.loaded_directly:
            self.ProjectFrame.hide()

        self.SaveToolButton: QToolButton
        if Project.loaded_directly:
            self.SaveToolButton.hide()

        self.CraftbotList: QListWidget
        for craftbot in sm.craft_editor.recipes:
            item = QListWidgetItem(craftbot.name)
            item.setData(QListWidgetItem.UserType, craftbot)

            pixmap = common.get_item_icon(craftbot.uuid)
            item.setIcon(QIcon(pixmap))

            self.CraftbotList.addItem(item)

    def _bindSignals(self):
        self.BackButton: QPushButton
        self.BackButton.clicked.connect(self._closePage)

        self.SaveToolButton: QToolButton
        self.SaveToolButton.clicked.connect(self._SaveToolButton_clicked)

        self.InstallButton: QPushButton
        self.InstallButton.clicked.connect(self._InstallButton_clicked)

        self.CraftbotList: QListWidget
        self.CraftbotList.itemDoubleClicked.connect(self._CraftbotList_itemDoubleClicked)

    def _closePage(self):
        PageManager.closeCurrentPage()
        self.closed.emit()

    # WIDGET'S EVENT SLOTS ##################################

    def _SaveToolButton_clicked(self):
        if Project.loaded_directly:
            return

        Project.save()

    def _InstallButton_clicked(self):
        Project.install()

    def _CraftbotList_itemDoubleClicked(self, item: QListWidgetItem):
        craftbot = item.data(QListWidgetItem.UserType)
        PageManager.openNewPage(RecipeListUi, craftbot=craftbot)
