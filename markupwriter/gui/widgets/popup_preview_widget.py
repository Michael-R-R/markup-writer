#!/usr/bin/python

import os

from PyQt6.QtCore import (
    QEvent,
    Qt,
)

from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
    QPushButton,
)

from markupwriter.config import ProjectConfig
from markupwriter.common.util import File
from . import DocumentEditorWidget


class PopupPreviewWidget(QWidget):
    def __init__(self, uuid: str, parent: QWidget | None) -> None:
        super().__init__(parent)

        self.setWindowFlag(Qt.WindowType.Popup)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setFixedSize(400, 200)
        
        self.previewButton = QPushButton("Preview...", self)
        self.previewButton.clicked.connect(lambda: self.close())

        self.textEdit = DocumentEditorWidget(self)
        self.textEdit.canResizeMargins = False
        self.textEdit.setMouseTracking(False)
        self.textEdit.setEnabled(True)
        self.textEdit.setReadOnly(True)
        path = os.path.join(ProjectConfig.contentPath(), uuid)
        self.textEdit.setPlainText(File.read(path))
        
        self.gLayout = QGridLayout(self)
        self.gLayout.addWidget(self.previewButton, 0, 0)
        self.gLayout.addWidget(self.textEdit, 1, 0)
        
    def leaveEvent(self, a0: QEvent | None) -> None:
        self.close()
        super().leaveEvent(a0)
