from PyQt6.QtCore import (
    QObject,
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

class AddItemAction(QAction):
    def __init__(self, parent: QObject):
        super().__init__(Icon.ADD_ITEM, "Add item", parent)