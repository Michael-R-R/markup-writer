#!/usr/bin/python

from PyQt6.QtCore import (
    Qt,
)

from PyQt6.QtGui import (
    QResizeEvent,
)

from PyQt6.QtWidgets import (
    QTreeWidget,
    QWidget,
    QFrame,
    QHBoxLayout,
    QVBoxLayout,
    QToolBar,
    QLabel,
)

from markupwriter.config import AppConfig
import markupwriter.gui.actions.doctree as dt


class DocumentTreeView(QWidget):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)
        
        self.titleLabel = QLabel("<b>Project Content<b>", self)

        toolbar = QToolBar(self)
        self.navUpAction = dt.ItemNavUpAction(toolbar)
        self.navDownAction = dt.ItemNavDownAction(toolbar)
        self.addItemAction = dt.ItemAddAction(toolbar)
        toolbar.addAction(self.navUpAction)
        toolbar.addAction(self.navDownAction)
        toolbar.addAction(self.addItemAction)
        self.toolbar = toolbar

        treewidget = QTreeWidget(self)
        treewidget.setDragEnabled(True)
        treewidget.setExpandsOnDoubleClick(False)
        treewidget.setUniformRowHeights(True)
        treewidget.setAllColumnsShowFocus(True)
        treewidget.setDragDropMode(QTreeWidget.DragDropMode.InternalMove)
        treewidget.setSelectionMode(QTreeWidget.SelectionMode.SingleSelection)
        treewidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        treewidget.setFrameStyle(QFrame.Shape.NoFrame)
        treewidget.setHeaderHidden(True)
        treewidget.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.treewidget = treewidget

        hLayout = QHBoxLayout()
        hLayout.addWidget(self.titleLabel)
        hLayout.addStretch()
        hLayout.addWidget(self.toolbar)
        self.hLayout = hLayout

        vLayout = QVBoxLayout(self)
        vLayout.addLayout(hLayout)
        vLayout.addWidget(self.treewidget)
        self.vLayout = vLayout
        
    def resizeEvent(self, e: QResizeEvent | None) -> None:
        AppConfig.docTreeSize = e.size()
        return super().resizeEvent(e)
