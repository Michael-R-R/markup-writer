#!/usr/bin/python

from PyQt6.QtWidgets import (
    QMessageBox,
    QWidget,
)


class ErrorDialog(object):
    def run(text: str, parent: QWidget | None):
        msgbox = QMessageBox(parent)
        msgbox.setText(text)
        msgbox.setIcon(QMessageBox.Icon.Critical)
        msgbox.exec()
