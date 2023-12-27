#!/usr/bin/python

from PyQt6.QtCore import (
    QDir,
)

from PyQt6.QtGui import (
    QIcon,
)

from PyQt6.QtWidgets import (
    QWidget,
    QTreeWidgetItem,
    QHBoxLayout,
    QLabel,
)

class DocumentTreeItem(QWidget):
    def __init__(self, title: str, path: str, 
                 item: QTreeWidgetItem, 
                 parent: QWidget):
        super().__init__(parent)

        self._path = path
        self._item = item

        hLayout = QHBoxLayout(self)
        hLayout.setContentsMargins(0, 0, 0, 0)

        self._title = QLabel(title, self)
        self._wordCount = QLabel("~", self)
        self._activeStatus = QLabel("~", self)
        self._groupStatus = QLabel("~", self)
        self._priorityStatus = QLabel("~", self)

        hLayout.addWidget(self._title)
        hLayout.addStretch()
        hLayout.addWidget(self._wordCount)
        hLayout.addWidget(self._activeStatus)
        hLayout.addWidget(self._groupStatus)
        hLayout.addWidget(self._priorityStatus)