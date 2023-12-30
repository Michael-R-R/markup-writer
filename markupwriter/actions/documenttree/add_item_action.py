from PyQt6.QtCore import (
    QObject,
    pyqtSignal,
)

from PyQt6.QtGui import (
    QAction,
)

from markupwriter.config import (
    HotkeyConfig,
)

from markupwriter.support.iconprovider import (
    Icon,
)

from markupwriter.widgetsupport.documenttree.treeitem import (
    BaseTreeItem,
)

from markupwriter.menus.documenttree import (
    AddItemMenu,
)

class AddItemAction(QAction):
    itemCreated = pyqtSignal(BaseTreeItem)

    def __init__(self, parent: QObject):
        super().__init__(Icon.ADD_ITEM, "Add item", parent)

        self._addItemMenu = AddItemMenu(None)
        self._addItemMenu.itemCreated.connect(lambda item: self.itemCreated.emit(item))
        self.setMenu(self._addItemMenu)