#!/usr/bin/python

from PyQt6.QtWidgets import (
    QInputDialog,
    QWidget,
    QLineEdit,
)

class StrDialog(object):
    def run(title: str, label: str, parent: QWidget | None) -> (str, bool):
        return QInputDialog.getText(parent,
                                    title,
                                    "Text",
                                    QLineEdit.EchoMode.Normal,
                                    label)