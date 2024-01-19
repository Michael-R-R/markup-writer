#!/usr/bin/python

from PyQt6.QtCore import (
    QEvent,
    Qt,
)

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
)

from markupwriter.config import AppConfig
from markupwriter.common.util import File
from . import DocumentTextEdit


class PreviewPopupWidget(QWidget):
    def __init__(self, uuid: str, parent: QWidget | None) -> None:
        super().__init__(parent)

        self.setWindowFlag(Qt.WindowType.Popup)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setFixedSize(400, 200)
        
        self.vLayout = QVBoxLayout(self)

        self.textedit = DocumentTextEdit(self)
        self.textedit.canResizeMargins = False
        self.textedit.setEnabled(True)
        self.textedit.setReadOnly(True)
        
        self.viewButton = QPushButton("View...", self)

        self.vLayout.addWidget(self.viewButton)
        self.vLayout.addWidget(self.textedit)

        path = AppConfig.projectContentPath() + uuid
        self.textedit.setPlainText(File.read(path))
        
    def leaveEvent(self, a0: QEvent | None) -> None:
        self.close()
        super().leaveEvent(a0)
