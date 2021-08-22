"""
...
"""
import os

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, pyqtBoundSignal
from PyQt5.QtWidgets import *

from core.project import Project
from core.ui.page_manager_class import PageManager
from core.ui.project_home_ui_class import ProjectHomeUi


class OpenProjectUi(QWidget):
    """..."""
    closed: pyqtBoundSignal = pyqtSignal()

    def __init__(self, parent: QWidget = None):
        QWidget.__init__(self, parent)
        uic.loadUi('core\\ui\\layout\\SMEOpenProject.ui', self)

        self._setupUi()
        self._bindSignals()
        self.show()

    def _setupUi(self):
        self.RecentProjectsList: QListWidget
        for path in Project.get_recent():
            lw_item = QListWidgetItem(path)
            lw_item.setData(QListWidgetItem.UserType, path)
            self.RecentProjectsList.addItem(lw_item)

    def _bindSignals(self):
        self.BrowseProjectToolButton: QToolButton
        self.BrowseProjectToolButton.clicked.connect(self._BrowseProjectToolButton_clicked)

        self.RecentProjectsList: QListWidget
        self.RecentProjectsList.itemClicked.connect(self._RecentProjectsList_itemClicked)
        self.RecentProjectsList.itemDoubleClicked.connect(self._RecentProjectsList_itemDoubleClicked)

        self.OpenProjectButton: QPushButton
        self.OpenProjectButton.clicked.connect(self._OpenProjectButton_clicked)

    # WIDGET'S EVENT SLOTS ##################################

    def _BrowseProjectToolButton_clicked(self):
        self.ProjectDirectoryLineEdit: QLineEdit
        path = QFileDialog.getExistingDirectory(self)
        if path == '':
            return
        self.ProjectDirectoryLineEdit.setText(path)

    def _RecentProjectsList_itemClicked(self, item: QListWidgetItem):
        path = item.data(QListWidgetItem.UserType)

        self.ProjectDirectoryLineEdit: QLineEdit
        self.ProjectDirectoryLineEdit.setText(path)

    def _RecentProjectsList_itemDoubleClicked(self, item: QListWidgetItem):
        self._OpenProjectButton_clicked()

    def _OpenProjectButton_clicked(self):
        self.ProjectDirectoryLineEdit: QLineEdit
        raw_path = self.ProjectDirectoryLineEdit.text()

        if raw_path == '' and QMessageBox.warning(
                    self,
                    'Invalid project path',
                    'Project path field can not be empty!'
                ):
            return

        path = os.path.expandvars(raw_path)
        if not os.path.exists(os.path.join(path, 'info.json')) and QMessageBox.warning(
                    self,
                    'Invalid project path',
                    'Given path does not exist'
                ):
            return

        Project.load(path)

        PageManager.closeCurrentPage()
        PageManager.openNewPage(ProjectHomeUi)
