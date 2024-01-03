#!/usr/bin/python

from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QToolBar,
    QLabel,
)

from markupwriter.actions.documenttree import (
    AddItemAction,
    NavUpAction,
    NavDownAction,
)

class DocumentTreeBar(QWidget):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        toolbar = QToolBar(self)
        self.navUpAction = NavUpAction(toolbar)
        self.navDownAction = NavDownAction(toolbar)
        self.addItemAction = AddItemAction(toolbar)
        toolbar.addAction(self.navUpAction)
        toolbar.addAction(self.navDownAction)
        toolbar.addAction(self.addItemAction)

        hLayout = QHBoxLayout(self)
        hLayout.setContentsMargins(0, 0, 0, 0)
        hLayout.addWidget(QLabel("<b>Project Content<b>", self))
        hLayout.addStretch()
        hLayout.addWidget(toolbar)
