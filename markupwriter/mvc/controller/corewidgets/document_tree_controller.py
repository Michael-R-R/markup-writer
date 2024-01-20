#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    QDataStream,
    pyqtSlot,
    pyqtSignal,
)

from PyQt6.QtWidgets import (
    QTreeWidget,
    QTreeWidgetItem,
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

from markupwriter.common.factory import (
    TreeItemFactory,
)

from markupwriter.config import (
    AppConfig,
)

from markupwriter.common.util import (
    File,
)

import markupwriter.support.doctree.item as dti


class DocumentTreeController(QObject):
    previewRequested = pyqtSignal(str, str)
    fileRenamed = pyqtSignal(str, str, str)
    
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
        
        # --- Tree signals --- #
        tree = self.view.treewidget
        tree.fileAdded.connect(self._onFileAdded)
        tree.fileRemoved.connect(self._onFileRemoved)

        # --- Tree context menu signals --- #
        tcm = self.view.treewidget.treeContextMenu
        tcm.addItemMenu.itemCreated.connect(self._onItemCreated)

        # --- Item context menu signals --- #
        icm = self.view.treewidget.itemContextMenu
        icm.addItemMenu.itemCreated.connect(self._onItemCreated)
        icm.previewAction.triggered.connect(self._onPreviewItem)
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
        
    def findTreeItem(self, uuid: str) -> dti.BaseTreeItem:
        return self.view.treewidget.findWidget(uuid)
        
    @pyqtSlot(str, list)
    def _onFileAdded(self, uuid: str, paths: list[str]):
        path = AppConfig.projectContentPath()
        if path is None:
            return
        path += uuid
        File.write(path, "")
    
    @pyqtSlot(str)
    def _onFileRemoved(self, uuid: str):
        path = AppConfig.projectContentPath()
        if path is None:
            return
        path += uuid
        File.remove(path)

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
    def _onPreviewItem(self):
        tree = self.view.treewidget
        item = tree.currentItem()
        if item is None:
            return
        
        widget: dti.BaseTreeItem = tree.itemWidget(item, 0)
        self.previewRequested.emit(widget.title(), widget.UUID())

    @pyqtSlot()
    def _onItemRename(self):
        tree = self.view.treewidget
        item = tree.currentItem()
        if item is None:
            return

        widget: dti.BaseTreeItem = tree.itemWidget(item, 0)
        text = StrDialog.run("Rename", widget.title(), None)
        if text is None:
            return

        oldTitle = widget.title()
        widget.setTitle(text)
        
        if widget.hasFlag(dti.ITEM_FLAG.file):
            self.fileRenamed.emit(widget.UUID(), oldTitle, text)

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
            tree.remove(item.child(i))

    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        
        # recursive helper
        def helper(sOut: QDataStream, tree: QTreeWidget, iParent: QTreeWidgetItem):
            cCount = iParent.childCount()
            sOut.writeInt(cCount)

            for i in range(cCount):
                iChild = iParent.child(i)
                wChild: dti.BaseTreeItem = tree.itemWidget(iChild, 0)
                sOut.writeQString(wChild.__class__.__name__)
                helper(sOut, tree, iChild)
                sOut << wChild
        
        tree = self.view.treewidget
        
        iCount = tree.topLevelItemCount()
        sout.writeInt(iCount)

        # Top level items
        for i in range(iCount):
            iParent = tree.topLevelItem(i)
            wParent: dti.BaseTreeItem = tree.itemWidget(iParent, 0)
            sout.writeQString(wParent.__class__.__name__)
            sout << wParent

            # Child level items
            helper(sout, tree, iParent)

        return sout

    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        
        # recursive helper
        def helper(sIn: QDataStream, tree: QTreeWidget, iParent: QTreeWidgetItem):
            cCount = sIn.readInt()

            for _ in range(cCount):
                type = sIn.readQString()
                wChild: dti.BaseTreeItem = TreeItemFactory.make(type)
                helper(sIn, tree, wChild.item)
                sIn >> wChild

                iParent.addChild(wChild.item)
                tree.setItemWidget(wChild.item, 0, wChild)
        
        tree = self.view.treewidget
        
        iCount = sin.readInt()

        # Top level items
        for i in range(iCount):
            type = sin.readQString()
            wParent: dti.BaseTreeItem = TreeItemFactory.make(type)
            sin >> wParent

            # Child level items
            helper(sin, tree, wParent.item)

            tree.addTopLevelItem(wParent.item)
            tree.setItemWidget(wParent.item, 0, wParent)

        return sin
