from PyQt6.QtWidgets import (
    QTreeWidget,
    QWidget,
)

class DocumentTree(QTreeWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)