#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    QDataStream,
    pyqtSlot,
)

from markupwriter.mvc.model.corewidgets import (
    DocumentTree,
)

from markupwriter.mvc.view.corewidgets import (
    DocumentTreeView,
)

from markupwriter.gui.dialogs.modal import (
    StrDialog,
    YesNoDialog,
)

import markupwriter.support.doctree.item as dti


class DocumentTreeController(QObject):
    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)

        self.model = DocumentTree(self)
        self.view = DocumentTreeView(None)
        
    def setup(self):
        tcm = self.view.treewidget.treeContextMenu
        tcm.addItemMenu.itemCreated.connect(self._onItemCreated)
        
        icm = self.view.treewidget.itemContextMenu
        icm.addItemMenu.itemCreated.connect(self._onItemCreated)
        icm.toggleActiveAction.triggered.connect(self._onItemToggleActive)
        icm.renameAction.triggered.connect(self._onItemRename)
        icm.toTrashAction.triggered.connect(self._onItemMoveToTrash)
        icm.recoverAction.triggered.connect(self._onItemRecover)
        
        trcm = self.view.treewidget.trashContextMenu
        trcm.emptyAction.triggered.connect(self._onEmptyTrash)
        
    @pyqtSlot(dti.BaseTreeItem)
    def _onItemCreated(self, item: dti.BaseTreeItem):
        self.view.treewidget.add(item)
        
    @pyqtSlot()
    def _onItemToggleActive(self):
        tree = self.view.treewidget
        item = tree.currentItem()
        if item is None:
            return

        widget: dti.BaseTreeItem = tree.itemWidget(item, 0)
        widget.toggleActive()
        
    @pyqtSlot()
    def _onItemRename(self):
        tree = self.view.treewidget
        item = tree.currentItem()
        if item is None:
            return

        widget: dti.BaseTreeItem = tree.itemWidget(item, 0)
        text = StrDialog.run("Rename", widget.title, None)
        if text is None:
            return

        widget.title = text
        
    @pyqtSlot()
    def _onItemMoveToTrash(self):
        tree = self.view.treewidget
        item = tree.currentItem()
        if item is None:
            return

        if not YesNoDialog.run("Move to trash?"):
            return

        trash = tree.findTrash()
        if trash is None:
            return

        tree.moveTo(item, trash)
        
    @pyqtSlot()
    def _onItemRecover(self):
        tree = self.view.treewidget
        item = tree.currentItem()
        if item is None:
            return
        
        tree.moveTo(item, None)
        
    @pyqtSlot()
    def _onEmptyTrash(self):
        tree = self.view.treewidget
        item = tree.currentItem()
        if item is None:
            return

        if not YesNoDialog.run("Empty trash?"):
            return

        for i in range(item.childCount() - 1, -1, -1):
            tree.remove(item.child(i), item)
        
    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        return sout
    
    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        return sin
