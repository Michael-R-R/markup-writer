#!/usr/bin/python

from markupwriter.contextmenus import (
    BaseContextMenu,
)

from markupwriter.widgetsupport.documenttree import (
    DocumentTree,
)

class TreeContextMenu(BaseContextMenu):
    def __init__(self, tree: DocumentTree):
        super().__init__()

        self._tree = tree

    def preprocess(self):
        raise NotImplementedError()