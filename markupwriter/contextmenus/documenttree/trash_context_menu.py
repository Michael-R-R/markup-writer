#!/usr/bin/python

from PyQt6.QtGui import (
    QAction,
)

from markupwriter.support.provider import (
    Icon,
)

from markupwriter.dialogs.modal import (
    YesNoDialog,
)

from markupwriter.widgetsupport.documenttree import (
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

    def _onEmptyTrash(self):
        trash = self._tree.findTrashFolder()
        if trash is None:
            return
        
        if not YesNoDialog.run("Empty trash?"):
            return
        
        for i in range(trash.childCount()-1, -1, -1):
            self._tree.removeItem(trash.child(i), trash)