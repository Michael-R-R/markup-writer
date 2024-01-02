#!/usr/bin/python

from PyQt6.QtGui import (
    QAction,
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
        self._menu.addAction(self.renameAction)
        self._menu.addAction(self.toTrashAction)

        self.addItemMenu.itemCreated.connect(self._onItemCreated)
        self.renameAction.triggered.connect(self._onRename)
        self.toTrashAction.triggered.connect(self._onMoveToTrash)

    def _onItemCreated(self, item: BaseTreeItem):
        self._tree.addItem(item)

    def _onRename(self):
        item = self._tree.currentItem()
        if item is None:
            return
        
        widget: BaseTreeItem = self._tree.itemWidget(item, 0)
        if not widget.isEditable:
            return

        text = StrDialog.run("Rename", widget.title, None)
        if text is None:
            return
        widget.title = text

    def _onMoveToTrash(self):
        item = self._tree.currentItem()
        if item is None:
            return
        
        widget: BaseTreeItem = self._tree.itemWidget(item, 0)
        if not widget.isEditable:
            return
        
        if not YesNoDialog.run("Move to trash?"):
            return
        
        trash = self._tree.findTrashFolder()
        if trash is None:
            return
        
        self._tree.moveItemTo(item, trash)