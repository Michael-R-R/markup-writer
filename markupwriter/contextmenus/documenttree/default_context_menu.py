#!/usr/bin/python

from markupwriter.menus.documenttree import (
    AddItemMenu,
)

from markupwriter.coresupport.documenttree import (
    DocumentTree,
)

from markupwriter.coresupport.documenttree.treeitem import (
    BaseTreeItem,
)

from .tree_context_menu import (
    TreeContextMenu,
)

class DefaultContextMenu(TreeContextMenu):
    def __init__(self, tree: DocumentTree):
        super().__init__(tree)

        self.addItemMenu = AddItemMenu(None)

        self._menu.addMenu(self.addItemMenu)

        self.addItemMenu.itemCreated.connect(self._onItemCreated)

    def preprocess(self):
        pass

    def postprocess(self):
        actions = self._menu.actions()
        for a in actions:
            a.setDisabled(False)
    
    def _onItemCreated(self, item: BaseTreeItem):
        self._tree.addWidget(item)