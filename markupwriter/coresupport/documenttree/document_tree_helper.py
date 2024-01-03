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
        self.tree = tree

        self._defaultContextMenu = DefaultContextMenu(self.tree)
        self._itemContextMenu = ItemContextMenu(self.tree)
        self._trashContextMenu = TrashContextMenu(self.tree)

    def onDragEnterEvent(self, super: QTreeView, e: QDragEnterEvent):
        item = self.tree.currentItem()
        widget: BaseTreeItem = self.tree.itemWidget(item, 0)
        if not widget.hasFlag(ITEM_FLAG.draggable):
            return
            
        self.tree.draggedItem = item

        super.dragEnterEvent(e)

    def onDropEvent(self, super: QTreeView, e: QDropEvent):
        if not self.tree.currentIndex().isValid():
            return
        
        item = self.tree.draggedItem
        if item is None:
            return
        
        itemList = self.tree.copyWidgets(item, list())
        super.dropEvent(e)
        self.tree.setItemWidgetList(itemList)
        self.tree.setCurrentItem(item)
        self.tree.expandItem(item)

        self.tree.draggedItem = None

    def onMousePressEvent(self, super: QTreeView, e: QMouseEvent):
        index = self.tree.indexAt(e.pos())
        super.mousePressEvent(e)
        if not index.isValid():
            self.tree.clearSelection()
            self.tree.setCurrentItem(None)

    def onItemDoubleClick(self, item: QTreeWidgetItem, col: int):
        widget: BaseTreeItem = self.tree.itemWidget(item, col)
        if widget.hasFlag(ITEM_FLAG.file):
            self.tree.fileDoubleClicked.emit(widget.shallowcopy())

    def onContextMenuRequest(self, pos: QPoint):
        item = self.tree.itemAt(pos)
        widget = self.tree.itemWidget(item, 0)
        pos = self.tree.mapToGlobal(pos)
        if item is None:
            self._defaultContextMenu.onShowMenu(pos)
        elif isinstance(widget, TrashFolderItem):
            self._trashContextMenu.onShowMenu(pos)
        else:
            self._itemContextMenu.onShowMenu(pos)
