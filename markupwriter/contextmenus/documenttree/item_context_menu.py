#!/usr/bin/python

from PyQt6.QtGui import (
    QAction,
)

from PyQt6.QtWidgets import (
    QTreeWidgetItem,
)

from markupwriter.support.provider import (
    Icon,
)

from markupwriter.menus.documenttree import (
    AddItemMenu,
)

from markupwriter.dialogs.modal import (
    StrDialog,
    YesNoDialog,
)

from markupwriter.widgetsupport.documenttree import (
    DocumentTree,
)

from markupwriter.widgetsupport.documenttree.treeitem import (
    ITEM_FLAG,
    BaseTreeItem,
)

from .tree_context_menu import (
    TreeContextMenu,
)

class ItemContextMenu(TreeContextMenu):
    def __init__(self, tree: DocumentTree) -> None:
        super().__init__(tree)

        self.addItemMenu = AddItemMenu(None)
        self._menu.addMenu(self.addItemMenu)

        self.renameAction = QAction("Rename")
        self.toTrashAction = QAction(Icon.TRASH_FOLDER, "Move to trash")
        self.recoverAction = QAction(Icon.TRASH_FOLDER, "Recover")
        self._menu.addAction(self.renameAction)
        self._menu.addAction(self.toTrashAction)
        self._menu.addAction(self.recoverAction)

        self.addItemMenu.itemCreated.connect(self._onItemCreated)
        self.renameAction.triggered.connect(self._onRename)
        self.toTrashAction.triggered.connect(self._onMoveToTrash)
        self.recoverAction.triggered.connect(self._onRecover)

    def preprocess(self):
        item = self._tree.currentItem()
        if item is None:
            return
        
        isInTrash = self._isInTrash(item)
        self.toTrashAction.setDisabled(isInTrash)
        self.recoverAction.setDisabled(not isInTrash)
            
        widget: BaseTreeItem = self._tree.itemWidget(item, 0)
        if not widget.hasFlag(ITEM_FLAG.mutable):
            self.renameAction.setDisabled(True)
            self.toTrashAction.setDisabled(True)

    def _onItemCreated(self, item: BaseTreeItem):
        self._tree.addWidget(item)

    def _onRename(self):
        item = self._tree.currentItem()
        if item is None:
            return
        
        widget: BaseTreeItem = self._tree.itemWidget(item, 0)
        text = StrDialog.run("Rename", widget.title, None)
        if text is None:
            return
        
        widget.title = text

    def _onMoveToTrash(self):
        item = self._tree.currentItem()
        if item is None:
            return
        
        if not YesNoDialog.run("Move to trash?"):
            return
        
        trash = self._tree.findTrashFolder()
        if trash is None:
            return
        
        self._tree.moveItemTo(item, trash)

    def _onRecover(self):
        item = self._tree.currentItem()
        if item is None:
            return
        self._tree.moveItemTo(item, None)

    def _isInTrash(self, item: QTreeWidgetItem) -> bool:
        trash = self._tree.findTrashFolder()

        prev = None
        curr = item.parent()
        while curr is not None:
            prev = curr
            curr = curr.parent()

        return prev == trash