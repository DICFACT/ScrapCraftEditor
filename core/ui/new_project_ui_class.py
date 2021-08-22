"""
...
"""
import os

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, pyqtBoundSignal
from PyQt5.QtWidgets import *

from core import gls
from core.project import PT_DEFAULT, PT_GAME_FILES, PT_EMPTY, Project
from core.ui.page_manager_class import PageManager
from core.ui.project_home_ui_class import ProjectHomeUi

from core.utils import tools

PROJECT_NAME_HINT = "Will be saved as: {PR_SYS_NAME}"

TEMPLATES = {
    "Default": PT_DEFAULT,
    "Game Files": PT_GAME_FILES,
    "Empty": PT_EMPTY
}


class NewProjectUi(QWidget):
    """..."""
    closed: pyqtBoundSignal = pyqtSignal()

    def __init__(self, parent: QWidget = None):
        QWidget.__init__(self, parent)
        uic.loadUi('core\\ui\\layout\\SMENewProject.ui', self)

        self._setupUi()
        self._bindSignals()
        self.show()

    def _setupUi(self):
        self.TemplateComboBox: QComboBox
        for name, template in TEMPLATES.items():
            self.TemplateComboBox.addItem(name, userData=template)

        self.ProjectNameHintLabel: QLabel
        self.ProjectNameHintLabel.hide()

        self.ProjectDirectoryLineEdit: QLineEdit
        self.ProjectDirectoryLineEdit.setText(gls.settings.get('default_project_path'))

    def _bindSignals(self):
        self.ProjectNameLineEdit: QLineEdit
        self.ProjectNameLineEdit.textChanged.connect(self._ProjectNameLineEdit_textChanged)

        self.CreateProjectButton: QPushButton
        self.CreateProjectButton.clicked.connect(self._CreateProjectButton_clicked)

        self.BrowseDirectoriesToolButton: QToolButton
        self.BrowseDirectoriesToolButton.clicked.connect(self._BrowseDirectoriesToolButton_clicked)

        self.GoHomeToolButton: QToolButton
        self.GoHomeToolButton.clicked.connect(self._GoHomeToolButton_clicked)

    # WIDGET'S EVENT SLOTS ##################################

    def _ProjectNameLineEdit_textChanged(self, text: str):
        system_name = tools.to_system_name(text)

        self.ProjectNameHintLabel: QLabel
        self.ProjectNameHintLabel.setHidden(system_name == text)
        self.ProjectNameHintLabel.setText(PROJECT_NAME_HINT.format(
            PR_SYS_NAME=system_name
        ))

    def _ProjectDirectoryLineEdit_returnPressed(self):
        pass

    def _BrowseDirectoriesToolButton_clicked(self):
        self.ProjectDirectoryLineEdit: QLineEdit
        path = QFileDialog.getExistingDirectory(self)
        if path == '':
            return
        self.ProjectDirectoryLineEdit.setText(path)

    def _GoHomeToolButton_clicked(self):
        self.ProjectDirectoryLineEdit: QLineEdit
        self.ProjectDirectoryLineEdit.setText(gls.settings.get('default_project_path'))

    def _AuthorNameLineEdit_returnPressed(self):
        pass

    def _CreateProjectButton_clicked(self):
        self.ProjectNameLineEdit: QLineEdit
        project_name = self.ProjectNameLineEdit.text()
        system_name = tools.to_system_name(project_name)

        self.ProjectDirectoryLineEdit: QLineEdit
        raw_path = self.ProjectDirectoryLineEdit.text()

        self.TemplateComboBox: QComboBox
        template = self.TemplateComboBox.currentData()

        self.AuthorNameLineEdit: QLineEdit
        author = self.AuthorNameLineEdit.text()

        # Data check and correction
        if (project_name == '' or system_name == '') and QMessageBox.warning(
                    self,
                    'Invalid project name',
                    'Project name field can not be empty!'
                ):
            return

        if raw_path == '' and QMessageBox.warning(
                    self,
                    'Invalid project path',
                    'Project path field can not be empty!'
                ):
            return

        projects_path = os.path.expandvars(raw_path)
        if not os.path.exists(projects_path) and QMessageBox.warning(
                    self,
                    'Invalid project path',
                    'Given path does not exist'
                ):
            return

        path = os.path.join(projects_path, system_name)
        if os.path.exists(path) and QMessageBox.question(
                    self,
                    'Overwrite?',
                    'Project with this name already exists,\nDo you want to overwrite it?',
                    QMessageBox.No | QMessageBox.Yes,
                    QMessageBox.No
                ) == QMessageBox.No:
            return

        if len(author) >= 64 and QMessageBox.warning(
                    self,
                    'Invalid author name',
                    'Content of "author" field must be less than 64 characters in length.\n'
                    'Please, try not to mention all your relatives!'
                ):
            return

        if len(project_name) >= 32 and QMessageBox.warning(
                    self,
                    'Invalid project name',
                    f'Content of "ProjectName" field must be less than 32 characters in length.\n'
                    f'You got {len(project_name)}, good job!'
                ):
            return

        # Finally, creating of a new project
        Project.new(project_name, system_name, author, projects_path, template)

        PageManager.closeCurrentPage()
        PageManager.openNewPage(ProjectHomeUi)
