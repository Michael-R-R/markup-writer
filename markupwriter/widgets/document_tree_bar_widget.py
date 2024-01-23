#!/usr/bin/python

from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
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

        self.hLayout = QHBoxLayout(self)
        self.hLayout.addWidget(self.titleLabel)
        self.hLayout.addStretch()
        self.hLayout.addWidget(self.toolbar)
        
        self.navUpAction.setEnabled(False)
        self.navDownAction.setEnabled(False)
        self.addItemAction.setEnabled(False)
