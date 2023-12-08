from PyQt6.QtGui import (
    QTextDocument,
)

from PyQt6.QtWidgets import (
    QPlainTextDocumentLayout,
)

class PlainDocument(QTextDocument):
    def __init__(self):
        super().__init__()
        
        self.setDocumentLayout(QPlainTextDocumentLayout(self))