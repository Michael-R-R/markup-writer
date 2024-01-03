#!/usr/bin/python

from PyQt6.QtGui import (
    QAction,
)

from markupwriter.common.provider import (
    Icon,
)

from markupwriter.dialogs.modal import (
    YesNoDialog,
)

from markupwriter.coresupport.documenttree import (
    DocumentTree,
)

from .tree_context_menu import (
    TreeContextMenu,
)

class TrashContextMenu(TreeContextMenu):
    def __init__(self, tree: DocumentTree) -> None:
        super().__init__(tree)

        self.emptyAction = QAction(Icon.TRASH_FOLDER, "Empty trash")

        self._menu.addAction(self.emptyAction)

        self.emptyAction.triggered.connect(self._onEmptyTrash)

    def preprocess(self):
        item = self._tree.currentItem()
        if item is None:
            return
        
        isEmpty = item.childCount() < 1
        self.emptyAction.setDisabled(isEmpty)

    def postprocess(self):
        actions = self._menu.actions()
        for a in actions:
            a.setDisabled(False)

    def _onEmptyTrash(self):
        item = self._tree.currentItem()
        if item is None:
            return
        
        if not YesNoDialog.run("Empty trash?"):
            return
        
        for i in range(item.childCount()-1, -1, -1):
            self._tree.removeItem(item.child(i), item)