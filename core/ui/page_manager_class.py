"""
...
"""
import typing as t

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QStackedLayout, QWidget


class PageManager(QStackedLayout):
    """..."""

    def __init__(self):
        QStackedLayout.__init__(self)

    def openNewPage(self, page_class: t.Type[QWidget], **kwargs):
        """Instantiates and opens new page"""
        parent: QObject = self.parent()
        page = page_class(parent, **kwargs)
        self.addWidget(page)
        self.setCurrentIndex(self.count() - 1)
        return page

    def openExistingPage(self, page: QWidget):
        """Opens existing page"""
        self.addWidget(page)
        self.setCurrentIndex(self.count() - 1)

    def closeCurrentPage(self):
        """Closes page that open right now"""
        self.removeWidget(self.currentWidget())


PageManager = PageManager()
