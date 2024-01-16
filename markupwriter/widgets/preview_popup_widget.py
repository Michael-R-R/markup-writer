#!/usr/bin/python

from PyQt6.QtCore import (
    Qt,
)

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPlainTextEdit,
)

from markupwriter.config import AppConfig
from markupwriter.common.util import File

class PreviewPopupWidget(QWidget):
    def __init__(self, uuid: str, parent: QWidget | None) -> None:
        super().__init__(parent)
        
        self.setWindowFlag(Qt.WindowType.Popup)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        
        self.textedit = QPlainTextEdit(self)
        self.textedit.setReadOnly(True)
        
        self.vLayout = QVBoxLayout(self)
        self.vLayout.addWidget(self.textedit)
        
        path = AppConfig.projectContentPath() + uuid
        content = File.read(path)
        self.textedit.setPlainText(content)
