#!/usr/bin/python

from PyQt6.QtCore import (
    Qt,
)

from PyQt6.QtGui import (
    QAction,
    QCursor,
)

from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel,
    QToolBar,
    QLineEdit,
)

from markupwriter.common.provider import Icon

import markupwriter.gui.actions.doctree as a
import markupwriter.gui.widgets as w


class DocumentTreeBarWidget(QWidget):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)

        self.titleLabel = QLabel("<b>Project Content<b>", self)

        self.toolbar = QToolBar(self)
        self.navUpAction = a.NavItemUpAction(self.toolbar)
        self.navDownAction = a.NavItemDownAction(self.toolbar)
        self.itemMenuAction = a.ItemMenuAction(self.toolbar)
        self.filterAction = QAction(Icon.FILTER, "Filter", self.toolbar)
        self.toolbar.addAction(self.navUpAction)
        self.toolbar.addAction(self.navDownAction)
        self.toolbar.addAction(self.itemMenuAction)
        self.toolbar.addAction(self.filterAction)
        
        self.navUpAction.setEnabled(False)
        self.navDownAction.setEnabled(False)
        self.itemMenuAction.setEnabled(False)
        self.filterAction.setEnabled(False)
        
        self.gLayout = QGridLayout(self)
        self.gLayout.addWidget(self.titleLabel, 0, 0, Qt.AlignmentFlag.AlignLeft)
        self.gLayout.addWidget(self.toolbar, 0, 1, Qt.AlignmentFlag.AlignRight)
        
        self.filterLineEdit = w.FilterLineEdit(self)
        self.filterAction.triggered.connect(self._onFilterAction)
        
    def _onFilterAction(self):
        pos = QCursor.pos()
        self.filterLineEdit.show()
        self.filterLineEdit.move(pos)
