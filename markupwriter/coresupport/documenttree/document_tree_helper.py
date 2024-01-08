#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    QPoint,
)

from PyQt6.QtWidgets import (
    QTreeView,
    QTreeWidgetItem,
)

from PyQt6.QtGui import (
    QDragEnterEvent,
    QDropEvent,
    QMouseEvent,
)

from markupwriter.dialogs.modal import (
    StrDialog,
    YesNoDialog,
)

from markupwriter.contextmenus.documenttree import (
    TreeContextMenu,
    ItemContextMenu,
    TrashContextMenu,
)

from .treeitem import (
    ITEM_FLAG,
    BaseTreeItem,
    TrashFolderItem,
)

import markupwriter.coresupport.documenttree as dt


class DocumentTreeHelper(QObject):
    def __init__(self, parent: dt.DocumentTree):
        super().__init__(parent)

        self._tree = parent

        self.treeContextMenu = TreeContextMenu(self)
        self.treeContextMenu.addItemMenu.itemCreated.connect(self.onItemCreated)

        self.itemContextMenu = ItemContextMenu(self)
        self.itemContextMenu.addItemMenu.itemCreated.connect(self.onItemCreated)
        self.itemContextMenu.toggleActiveAction.triggered.connect(self.onToggleActive)
        self.itemContextMenu.renameAction.triggered.connect(self.onRename)
        self.itemContextMenu.toTrashAction.triggered.connect(self.onMoveToTrash)
        self.itemContextMenu.recoverAction.triggered.connect(self.onRecover)

        self.trashContextMenu = TrashContextMenu(self)
        self.trashContextMenu.emptyAction.triggered.connect(self.onEmptyTrash)

    def onDragEnterEvent(self, super: QTreeView, e: QDragEnterEvent):
        item = self._tree.currentItem()
        widget: BaseTreeItem = self._tree.itemWidget(item, 0)
        if not widget.hasFlag(ITEM_FLAG.draggable):
            return

        self._tree.draggedItem = item

        super.dragEnterEvent(e)

    def onDropEvent(self, super: QTreeView, e: QDropEvent):
        if not self._tree.currentIndex().isValid():
            return

        item = self._tree.draggedItem
        if item is None:
            return

        itemList = self._tree.copyWidgets(item, list())
        super.dropEvent(e)
        self._tree.setWidgetList(itemList)
        self._tree.setCurrentItem(item)
        self._tree.expandItem(item)

        self._tree.draggedItem = None

    def onMousePressEvent(self, super: QTreeView, e: QMouseEvent):
        index = self._tree.indexAt(e.pos())
        super.mousePressEvent(e)
        if not index.isValid():
            self._tree.clearSelection()
            self._tree.setCurrentItem(None)

    def onItemDoubleClick(self, item: QTreeWidgetItem, col: int):
        paths: list[str] = list()
        iTemp = item
        while iTemp is not None:
            wTemp: BaseTreeItem = self._tree.itemWidget(iTemp, 0)
            paths.insert(0, wTemp.title)
            iTemp = iTemp.parent()
        
        widget: BaseTreeItem = self._tree.itemWidget(item, col)
        if widget.hasFlag(ITEM_FLAG.file):
            self._tree.fileDoubleClicked.emit(widget.UUID(), paths)

    def onContextMenuRequest(self, pos: QPoint):
        item = self._tree.itemAt(pos)
        widget: BaseTreeItem = self._tree.itemWidget(item, 0)
        pos = self._tree.mapToGlobal(pos)
        if item is None:
            self.treeContextMenu.onShowMenu(pos)
        elif isinstance(widget, TrashFolderItem):
            isEmpty = item.childCount() < 1
            args = [isEmpty]
            self.trashContextMenu.onShowMenu(pos, args)
        else:
            inTrash = self._tree.isInTrash(item)
            isMutable = widget.hasFlag(ITEM_FLAG.mutable)
            args = [inTrash, isMutable]
            self.itemContextMenu.onShowMenu(pos, args)

    def onItemCreated(self, item: BaseTreeItem):
        self._tree.add(item)

    def onToggleActive(self):
        item = self._tree.currentItem()
        if item is None:
            return

        widget: BaseTreeItem = self._tree.itemWidget(item, 0)
        widget.toggleActive()

    def onRename(self):
        item = self._tree.currentItem()
        if item is None:
            return

        widget: BaseTreeItem = self._tree.itemWidget(item, 0)
        text = StrDialog.run("Rename", widget.title, None)
        if text is None:
            return

        widget.title = text

    def onMoveToTrash(self):
        item = self._tree.currentItem()
        if item is None:
            return

        if not YesNoDialog.run("Move to trash?"):
            return

        trash = self._tree.findTrash()
        if trash is None:
            return

        self._tree.moveTo(item, trash)

    def onRecover(self):
        item = self._tree.currentItem()
        if item is None:
            return
        self._tree.moveTo(item, None)

    def onEmptyTrash(self):
        item = self._tree.currentItem()
        if item is None:
            return

        if not YesNoDialog.run("Empty trash?"):
            return

        for i in range(item.childCount() - 1, -1, -1):
            self._tree.remove(item.child(i), item)
