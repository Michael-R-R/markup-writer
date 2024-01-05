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

        self._treeContextMenu = TreeContextMenu(self)
        self._treeContextMenu.addItemMenu.itemCreated.connect(self.onItemCreated)

        self._itemContextMenu = ItemContextMenu(self)
        self._itemContextMenu.addItemMenu.itemCreated.connect(self.onItemCreated)
        self._itemContextMenu.toggleActiveAction.triggered.connect(self.onToggleActive)
        self._itemContextMenu.renameAction.triggered.connect(self.onRename)
        self._itemContextMenu.toTrashAction.triggered.connect(self.onMoveToTrash)
        self._itemContextMenu.recoverAction.triggered.connect(self.onRecover)

        self._trashContextMenu = TrashContextMenu(self)
        self._trashContextMenu.emptyAction.triggered.connect(self.onEmptyTrash)

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
        self._tree.setItemWidgetList(itemList)
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
        widget: BaseTreeItem = self._tree.itemWidget(item, col)
        if widget.hasFlag(ITEM_FLAG.file):
            self._tree.fileDoubleClicked.emit(widget.UUID())

    def onContextMenuRequest(self, pos: QPoint):
        item = self._tree.itemAt(pos)
        widget: BaseTreeItem = self._tree.itemWidget(item, 0)
        pos = self._tree.mapToGlobal(pos)
        if item is None:
            self._treeContextMenu.onShowMenu(pos)
        elif isinstance(widget, TrashFolderItem):
            isEmpty = item.childCount() < 1
            args = [isEmpty]
            self._trashContextMenu.onShowMenu(pos, args)
        else:
            inTrash = self._tree.isItemInTrash(item)
            isMutable = widget.hasFlag(ITEM_FLAG.mutable)
            args = [inTrash, isMutable]
            self._itemContextMenu.onShowMenu(pos, args)

    def onItemCreated(self, item: BaseTreeItem):
        self._tree.addItemWidget(item)

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
        
        trash = self._tree.findTrashFolder()
        if trash is None:
            return
        
        self._tree.moveItemTo(item, trash)

    def onRecover(self):
        item = self._tree.currentItem()
        if item is None:
            return
        self._tree.moveItemTo(item, None)

    def onEmptyTrash(self):
        item = self._tree.currentItem()
        if item is None:
            return
        
        if not YesNoDialog.run("Empty trash?"):
            return
        
        for i in range(item.childCount()-1, -1, -1):
            self._tree.removeItem(item.child(i), item)
