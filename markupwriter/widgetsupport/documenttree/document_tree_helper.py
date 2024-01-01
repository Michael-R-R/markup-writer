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

from .treeitem import (
    BaseTreeItem,
)

from markupwriter.dialogs.modal import (
    StrDialog,
    YesNoDialog,
)

from .treeitem import (
    TrashFolderItem,
)

import markupwriter.widgetsupport.documenttree as dt

class DocumentTreeHelper(object):
    def __init__(self, tree: dt.DocumentTree):
        self.tree = tree

    def onDragEnterEvent(self, super: QTreeView, e: QDragEnterEvent):
        item = self.tree.currentItem()
        widget: BaseTreeItem = self.tree.itemWidget(item, 0)
        if not widget.isDraggable:
            return
            
        self.tree.draggedItem = item

        super.dragEnterEvent(e)

    def onDropEvent(self, super: QTreeView, e: QDropEvent):
        if not self.tree.currentIndex().isValid():
            return
        
        item = self.tree.draggedItem
        if self.tree.draggedItem is None:
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
        if not widget.isFolder():
            self.tree.fileDoubleClicked.emit(widget.shallowcopy())

    def onContextMenuRequest(self, pos: QPoint):
        item = self.tree.itemAt(pos)
        widget = self.tree.itemWidget(item, 0)
        pos = self.tree.mapToGlobal(pos)
        if item is None:
            self.tree.contextMenu.onEmptyClickMenu(pos)
        elif isinstance(widget, TrashFolderItem):
            self.tree.contextMenu.onTrashFolderMenu(pos)
        else:
            self.tree.contextMenu.onBaseItemMenu(pos)

    def onRenameItem(self):
        item = self.tree.currentItem()
        if item is None:
            return
        
        widget: BaseTreeItem = self.tree.itemWidget(item, 0)
        if not widget.isEditable:
            return

        text = StrDialog.run("Rename", widget.title, None)
        if text is None:
            return
        widget.title = text

    def onMoveToTrash(self):
        if not YesNoDialog.run("Move to trash?"):
            return

        item = self.tree.currentItem()
        if item is None:
            return
        
        widget: BaseTreeItem = self.tree.itemWidget(item, 0)
        if not widget.isEditable:
            return
        
        trash = self.tree.findTrashFolder()
        if trash is None:
            return
        
        self.tree.moveItemTo(item, trash)

    def onEmptyTrash(self):
        if not YesNoDialog.run("Empty trash?"):
            return

        trash = self.tree.findTrashFolder()
        if trash is None:
            return
        
        for i in range(trash.childCount()-1, -1, -1):
            self.tree.removeItem(trash.child(i), trash)
