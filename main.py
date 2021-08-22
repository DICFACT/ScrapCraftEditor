"""
...
"""
import os

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

from core import gls
from core.ui.main_menu_ui_class import MainMenuUi
from core.ui.page_manager_class import PageManager


def main():
    """Point of entry"""
    import sys

    # SETTING UP SOME THINGS ############################
    gls.window_settings.load(gls.WINDOW_SETTINGS)
    gls.settings.load(gls.SETTINGS)

    os.environ['SMCE'] = os.path.join(os.getcwd(), 'user')
    os.environ['SM_ROOT'] = gls.settings.get('game_root')
    # ###################################################

    app = QApplication(sys.argv)

    main_window = QMainWindow()
    main_window.hide()

    width, height = gls.window_settings.get("default_geometry")
    main_window.setFixedSize(width, height)

    title = gls.window_settings.get("main_window_title")
    main_window.setWindowTitle(title.format(**gls.APP_INFO))

    central_widget = QWidget()
    central_widget.setLayout(PageManager)
    main_window.setCentralWidget(central_widget)

    main_window.show()

    PageManager.openNewPage(MainMenuUi)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
