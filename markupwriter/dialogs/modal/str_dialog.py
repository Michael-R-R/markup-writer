#!/usr/bin/python

from PyQt6.QtWidgets import (
    QInputDialog,
    QWidget,
    QLineEdit,
)

class StrDialog(object):
    def run(title: str, label: str, parent: QWidget | None) -> str | None:
        result = QInputDialog.getText(parent,
                                      title,
                                      "Text",
                                      QLineEdit.EchoMode.Normal,
                                      label)
        if not result[1]:
            return None
        
        return result[0]