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
        self.resultList.itemDoubleClicked.connect(self._onFileOpened)

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
        
        self.resultList.setCurrentRow(0)

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
    def _onFileOpened(self, item: QListWidgetItem):
        if item is None:
            return
        
        key = item.text()
        if not key in self.collection:
            return
        
        widget: ti.BaseTreeItem = self.collection[key]
        self.tree.fileOpened.emit(widget.UUID(), key[1:].split("/"))
        
        self.close()
        
    @pyqtSlot(QListWidgetItem)
    def _onFilePreviewed(self, item: QListWidgetItem):
        if item is None:
            return
        
        key = item.text()
        if not key in self.collection:
            return
        
        widget: ti.BaseTreeItem = self.collection[key]
        self.tree.filePreviewed.emit(widget.title(), widget.UUID())
        
        self.close()
        
    def _toggleSearchFocus(self):
        if self.searchLine.hasFocus():
            self.searchLine.clearFocus()
            self._navigateList(0)
        else:
            self.searchLine.setFocus()
    
    def _navigateList(self, direction: int):
        count = self.resultList.count()
        if count < 1:
            return
        
        row = self.resultList.currentRow()
        row = (row + direction) % count
        
        self.resultList.setCurrentRow(row)
        
    def _scrollPreviewY(self, direction: int):
        vb = self.preview.verticalScrollBar()
        if vb is None:
            return
        val = vb.value()
        vb.setValue(val + (16 * direction))

    def keyPressEvent(self, e: QKeyEvent | None) -> None:
        match e.key():
            case Qt.Key.Key_Escape:
                self.close()
            case Qt.Key.Key_Return:
                self._toggleSearchFocus()
            case Qt.Key.Key_W:
                self._navigateList(-1)
            case Qt.Key.Key_S:
                self._navigateList(1)
            case Qt.Key.Key_K:
                self._scrollPreviewY(-1)
            case Qt.Key.Key_J:
                self._scrollPreviewY(1)
            case Qt.Key.Key_O:
                self._onFileOpened(self.resultList.currentItem())
            case Qt.Key.Key_P:
                self._onFilePreviewed(self.resultList.currentItem())
            case _:
                return super().keyPressEvent(e)
