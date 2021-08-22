"""
...
"""
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, pyqtBoundSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *

from core.project import Project
from core.ui.new_project_ui_class import NewProjectUi
from core.ui.open_project_ui_class import OpenProjectUi
from core.ui.page_manager_class import PageManager
from core.ui.project_home_ui_class import ProjectHomeUi

INVALID_GAME_ROOT_PATH = {
    "title": 'Warning',
    "message": 'This path either does not exist or does not lead to the root folder of the ScrapMechanic game.\n'
               'Please select correct directory.'
}


class MainMenuUi(QWidget):
    """..."""
    closed: pyqtBoundSignal = pyqtSignal()

    def __init__(self, parent: QWidget = None):
        QWidget.__init__(self, parent)
        uic.loadUi('core\\ui\\layout\\SMEMainMenu.ui', self)

        self._setupUi()
        self._bindSignals()
        self.show()

    def _setupUi(self):
        self.GameDirectoryWidget: QWidget
        self.GameDirectoryWidget.hide()

        self.SMELogoLarge: QLabel
        self.SMELogoLarge.setPixmap(QPixmap('core/res/mm_logo.png'))

    def _bindSignals(self):
        self.EditGameDirectoryToolButton: QToolButton
        self.EditGameDirectoryToolButton.toggled.connect(self._EditGameDirectoryToolButton_toggled)

        self.GameDirectoryLineEdit: QLineEdit
        self.GameDirectoryLineEdit.returnPressed.connect(self._GameDirectoryLineEdit_returnPressed)

        self.NewProjectButton: QPushButton
        self.NewProjectButton.clicked.connect(self._NewProjectButton_clicked)

        self.OpenProjectButton: QPushButton
        self.OpenProjectButton.clicked.connect(self._OpenProjectButton_clicked)

        self.EditGameFilesButton: QPushButton
        self.EditGameFilesButton.clicked.connect(self._EditGameFilesButton_clicked)

    # WIDGET'S EVENT SLOTS ##################################

    def _NewProjectButton_clicked(self):
        """..."""
        PageManager.openNewPage(NewProjectUi)

    def _OpenProjectButton_clicked(self):
        """..."""
        PageManager.openNewPage(OpenProjectUi)

    def _EditGameFilesButton_clicked(self):
        """..."""
        Project.load_gf()
        PageManager.openNewPage(ProjectHomeUi)

    def _EditGameDirectoryToolButton_toggled(self, checked: bool):
        self.GameDirectoryWidget: QWidget
        self.GameDirectoryWidget.setHidden(not checked)

    def _GameDirectoryLineEdit_returnPressed(self):
        import os
        self.GameDirectoryLineEdit: QLineEdit
        directory = self.GameDirectoryLineEdit.text()
        if not os.path.exists(os.path.join(directory, 'Release\\ScrapMechanic.exe')):
            QMessageBox.warning(
                self,
                INVALID_GAME_ROOT_PATH['title'],
                INVALID_GAME_ROOT_PATH['message'],
                QMessageBox.Ok
            )
            return
        print(directory)
        # TODO: Implement methods 'set' and 'save' in Settings class, then uncomment this
        # gls.settings.set('game_root', directory)
        # gls.settings.save(gls.SETTINGS)
