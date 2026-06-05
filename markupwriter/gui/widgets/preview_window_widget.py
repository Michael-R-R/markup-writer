#!/usr/bin/python

from PyQt6.QtCore import (
    Qt,
)

from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
    QSizePolicy,
)

from markupwriter.gui.widgets import PreviewWidget

class PreviewWindowWidget(QWidget):
    def __init__(self, title: str, uuid: str, parent: QWidget | None) -> None:
        super().__init__(parent, Qt.WindowType.Window)

        self.setWindowTitle(title)
        self.resize(800, 900)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        self.previewWidget = PreviewWidget(title, uuid, self)

        self.gLayout = QGridLayout(self)
        self.gLayout.addWidget(self.previewWidget, 0, 0)