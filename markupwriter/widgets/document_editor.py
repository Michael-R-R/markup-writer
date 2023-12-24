#!/usr/bin/python

from PyQt6.QtGui import (
    QResizeEvent,
    QTextCursor,
)

from PyQt6.QtWidgets import (
    QPlainTextEdit,
    QWidget,
)

from markupwriter.config import AppConfig

from markupwriter.widgetsupport.documenteditor import (
    PlainDocument,
)

from markupwriter.support.editorparser import (
    ActiveEditorParser,
)

class DocumentEditor(QPlainTextEdit):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.__document = PlainDocument()
        self.__activeParser = ActiveEditorParser()
        
        self.setDocument(self.__document)
        self.setTabStopDistance(20.0)

        self.textChanged.connect(self.onTextChanged)

    def resizeEvent(self, e: QResizeEvent | None) -> None:
        AppConfig.docEditorSize = e.size()
        return super().resizeEvent(e)
    
    def onTextChanged(self):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.EndOfLine)
        cursor.select(QTextCursor.SelectionType.LineUnderCursor)
        self.__activeParser.tokenize(self.__document, 
                                     "todo/add/real/activepath.doc",
                                     cursor.selectedText())