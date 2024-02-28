#!/usr/bin/python

import re

from PyQt6.QtCore import (
    Qt,
    pyqtSlot,
)

from PyQt6.QtGui import (
    QKeyEvent,
)

from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
    QListWidget,
    QLineEdit,
    QPlainTextEdit,
    QTreeWidgetItem,
    QListWidgetItem,
)

from markupwriter.common.util import File
from markupwriter.config import ProjectConfig

import markupwriter.support.doctree.item as ti
import markupwriter.gui.widgets as w


class TelescopeWidget(QWidget):
    def __init__(self, tree: w.DocumentTreeWidget, parent: QWidget | None) -> None:
        super().__init__(parent)

        self.setWindowFlag(Qt.WindowType.Popup)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        self.tree = tree
        self.collection = dict()

        self.searchLine = QLineEdit(self)
        self.resultList = QListWidget(self)
        self.preview = QPlainTextEdit(self)

        self.gLayout = QGridLayout(self)
        self.gLayout.addWidget(self.searchLine, 0, 0, 1, 2)
        self.gLayout.addWidget(self.resultList, 2, 0)
        self.gLayout.addWidget(self.preview, 2, 1)

        self.searchLine.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.preview.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.searchLine.textChanged.connect(self._filterSearch)
        self.resultList.currentItemChanged.connect(self._onCurrentItemChanged)
        self.resultList.itemDoubleClicked.connect(self._onItemSelected)

        self._buildCollection(tree)
        
        self.searchLine.setFocus()

    def _buildCollection(self, tree: w.DocumentTreeWidget):
        def helper(pitem: QTreeWidgetItem, path: str):
            pwidget: ti.BaseTreeItem = tree.itemWidget(pitem, 0)
            path = "{}/{}".format(path, pwidget.title())

            for i in range(pitem.childCount()):
                helper(pitem.child(i), path)

            if not pwidget.hasFlag(ti.ITEM_FLAG.file):
                return

            self.collection[path] = pwidget

        # End helper

        for i in range(tree.topLevelItemCount()):
            item = tree.topLevelItem(i)
            helper(item, "")

    @pyqtSlot(str)
    def _filterSearch(self, text: str):
        self.resultList.clear()

        if text == "":
            return

        regex = re.compile(text, re.IGNORECASE)
        for key in self.collection:
            found = regex.search(key)
            if found is None:
                continue

            item = QListWidgetItem()
            item.setText(key)
            self.resultList.insertItem(0, item)

    @pyqtSlot(QListWidgetItem, QListWidgetItem)
    def _onCurrentItemChanged(self, curr: QListWidgetItem, prev: QListWidgetItem):
        self.preview.clear()
        
        if curr is None:
            return
        
        key = curr.text()
        if not key in self.collection:
            return
        
        widget: ti.BaseTreeItem = self.collection[key]
        path = ProjectConfig.contentPath() + widget.UUID()
        content = File.read(path)
        if content is None:
            return
        
        self.preview.setPlainText(content)

    @pyqtSlot(QListWidgetItem)
    def _onItemSelected(self, item: QListWidgetItem):
        if item is None:
            return
        
        key = item.text()
        if not key in self.collection:
            return
        
        widget: ti.BaseTreeItem = self.collection[key]
        self.tree.fileOpened.emit(widget.UUID(), key[1:].split("/"))
        
        self.close()
    
    def _navigateList(self, direction: int):
        count = self.resultList.count()
        row = self.resultList.currentRow()
        row = (row + direction) % count
        
        self.resultList.setCurrentRow(row)

    def keyPressEvent(self, e: QKeyEvent | None) -> None:
        match e.key():
            case Qt.Key.Key_Escape:
                self.close()
            case Qt.Key.Key_Up:
                self._navigateList(-1)
            case Qt.Key.Key_Down:
                self._navigateList(1)
            case Qt.Key.Key_Return:
                self._onItemSelected(self.resultList.currentItem())

        return super().keyPressEvent(e)
