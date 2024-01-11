#!/usr/bin/python

from PyQt6.QtCore import (
    Qt,
)

from PyQt6.QtWidgets import (
    QTreeWidget,
    QWidget,
    QFrame,
)


class DocumentTreeWidget(QTreeWidget):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)

        self.setDragEnabled(True)
        self.setExpandsOnDoubleClick(False)
        self.setUniformRowHeights(True)
        self.setAllColumnsShowFocus(True)
        self.setDragDropMode(QTreeWidget.DragDropMode.InternalMove)
        self.setSelectionMode(QTreeWidget.SelectionMode.SingleSelection)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setHeaderHidden(True)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
