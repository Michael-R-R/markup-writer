#!/usr/bin/python

from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QToolBar,
    QLabel,
)

from markupwriter.actions.documenttree import (
    ItemAddAction,
    ItemNavUpAction,
    ItemNavDownAction,
)

class DocumentTreeBar(QWidget):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        toolbar = QToolBar(self)
        self.navUpAction = ItemNavUpAction(toolbar)
        self.navDownAction = ItemNavDownAction(toolbar)
        self.addItemAction = ItemAddAction(toolbar)
        toolbar.addAction(self.navUpAction)
        toolbar.addAction(self.navDownAction)
        toolbar.addAction(self.addItemAction)

        hLayout = QHBoxLayout(self)
        hLayout.setContentsMargins(0, 0, 0, 0)
        hLayout.addWidget(QLabel("<b>Project Content<b>", self))
        hLayout.addStretch()
        hLayout.addWidget(toolbar)
