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
        self.setActionStates(False)
        
        # --- Tree bar signals --- #
        treebar = self.view.treebar
        treebar.addItemAction.itemCreated.connect(self._onItemCreated)
        treebar.navUpAction.triggered.connect(self._onItemNavUp)
        treebar.navDownAction.triggered.connect(self._onItemNavDown)

        # --- Tree context menu signals --- #
        tcm = self.view.treewidget.treeContextMenu
        tcm.addItemMenu.itemCreated.connect(self._onItemCreated)

        # --- Item context menu signals --- #
        icm = self.view.treewidget.itemContextMenu
        icm.addItemMenu.itemCreated.connect(self._onItemCreated)
        icm.toggleActiveAction.triggered.connect(self._onItemToggleActive)
        icm.renameAction.triggered.connect(self._onItemRename)
        icm.toTrashAction.triggered.connect(self._onItemMoveToTrash)
        icm.recoverAction.triggered.connect(self._onItemRecover)

        # --- Trash context menu signals --- #
        trcm = self.view.treewidget.trashContextMenu
        trcm.emptyAction.triggered.connect(self._onEmptyTrash)
        
    def setActionStates(self, isEnabled: bool):
        # --- Tree bar --- #
        treeBar = self.view.treebar
        treeBar.navUpAction.setEnabled(isEnabled)
        treeBar.navDownAction.setEnabled(isEnabled)
        treeBar.addItemAction.setEnabled(isEnabled)

        # --- Tree --- #
        tree = self.view.treewidget
        tree.treeContextMenu.addItemMenu.setEnabled(isEnabled)
        
    def createRootFolders(self):
        tree = self.view.treewidget
        tree.add(dti.PlotFolderItem())
        tree.add(dti.TimelineFolderItem())
        tree.add(dti.CharsFolderItem())
        tree.add(dti.LocFolderItem())
        tree.add(dti.ObjFolderItem())
        tree.add(dti.TrashFolderItem()) 

    @pyqtSlot()
    def _onItemNavUp(self):
        self.view.treewidget.translate(-1)

    @pyqtSlot()
    def _onItemNavDown(self):
        self.view.treewidget.translate(1)

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
