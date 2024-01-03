#!/usr/bin/python

from PyQt6.QtCore import (
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

from markupwriter.contextmenus.documenttree import (
    DefaultContextMenu,
    ItemContextMenu,
    TrashContextMenu,
)

from .treeitem import (
    ITEM_FLAG,
    BaseTreeItem,
    TrashFolderItem,
)

import markupwriter.coresupport.documenttree as dt

class DocumentTreeHelper(object):
    def __init__(self, tree: dt.DocumentTree):
        self._tree = tree

        self._defaultContextMenu = DefaultContextMenu(self._tree)
        self._itemContextMenu = ItemContextMenu(self._tree)
        self._trashContextMenu = TrashContextMenu(self._tree)

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
            self._tree.fileDoubleClicked.emit(widget)

    def onContextMenuRequest(self, pos: QPoint):
        item = self._tree.itemAt(pos)
        widget = self._tree.itemWidget(item, 0)
        pos = self._tree.mapToGlobal(pos)
        if item is None:
            self._defaultContextMenu.onShowMenu(pos)
        elif isinstance(widget, TrashFolderItem):
            self._trashContextMenu.onShowMenu(pos)
        else:
            self._itemContextMenu.onShowMenu(pos)
