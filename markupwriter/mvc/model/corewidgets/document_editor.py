#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
)

import markupwriter.support.doceditor as de


class DocumentEditor(QObject):
    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)

        self.currDocPath = ""
        self.currDocUUID = ""
