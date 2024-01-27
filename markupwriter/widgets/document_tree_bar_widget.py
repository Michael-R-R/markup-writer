#!/usr/bin/python

from PyQt6.QtCore import (
    Qt,
)

from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel,
    QToolBar,
)

import markupwriter.gui.actions.doctree as dt


class DocumentTreeBarWidget(QWidget):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)

        self.titleLabel = QLabel("<b>Project Content<b>", self)

        self.toolbar = QToolBar(self)
        self.navUpAction = dt.ItemNavUpAction(self.toolbar)
        self.navDownAction = dt.ItemNavDownAction(self.toolbar)
        self.addItemAction = dt.ItemAddAction(self.toolbar)
        self.toolbar.addAction(self.navUpAction)
        self.toolbar.addAction(self.navDownAction)
        self.toolbar.addAction(self.addItemAction)
        
        self.gLayout = QGridLayout(self)
        self.gLayout.addWidget(self.titleLabel, 0, 0, Qt.AlignmentFlag.AlignLeft)
        self.gLayout.addWidget(self.toolbar, 0, 1, Qt.AlignmentFlag.AlignRight)
        
        self.navUpAction.setEnabled(False)
        self.navDownAction.setEnabled(False)
        self.addItemAction.setEnabled(False)
