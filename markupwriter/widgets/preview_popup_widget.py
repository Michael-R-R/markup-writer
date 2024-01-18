#!/usr/bin/python

from PyQt6.QtCore import (
    QEvent,
    Qt,
)

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTextEdit,
)

from markupwriter.config import AppConfig
from markupwriter.common.util import File


class PreviewPopupWidget(QWidget):
    def __init__(self, uuid: str, parent: QWidget | None) -> None:
        super().__init__(parent)

        self.setWindowFlag(Qt.WindowType.Popup)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setFixedSize(400, 200)

        self.textedit = QTextEdit(self)
        self.textedit.setReadOnly(True)

        self.vLayout = QVBoxLayout(self)
        self.vLayout.addWidget(self.textedit)

        path = AppConfig.projectContentPath() + uuid
        content = File.read(path)
        # TODO parse to html
        self.textedit.setHtml(content)
        
    def leaveEvent(self, a0: QEvent | None) -> None:
        self.close()
        return super().leaveEvent(a0)
