#!/usr/bin/python

from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QToolBar,
    QLabel,
)

from markupwriter.actions.documenttree import (
    NavUpAction,
    NavDownAction,
)

class DocumentTreeBar(QWidget):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        toolbar = QToolBar(self)
        self.navUpAction = NavUpAction(toolbar)
        self.navDownAction = NavDownAction(toolbar)
        toolbar.addAction(self.navUpAction)
        toolbar.addAction(self.navDownAction)

        hLayout = QHBoxLayout(self)
        hLayout.setContentsMargins(0, 0, 0, 0)
        hLayout.addWidget(QLabel("<b>Project Content<b>", self))
        hLayout.addStretch()
        hLayout.addWidget(toolbar)
