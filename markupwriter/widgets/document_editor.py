from PyQt6.QtWidgets import (
    QPlainTextEdit,
    QWidget,
)

from markupwriter.widgetsupport.documenteditor.plain_document import (
    PlainDocument,
)

class DocumentEditor(QPlainTextEdit):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.setDocument(PlainDocument())