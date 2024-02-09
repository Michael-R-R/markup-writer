#!/usr/bin/python

from PyQt6.QtWidgets import (
    QMessageBox,
    QWidget,
)


class ErrorDialog(object):
    def run(text: str, parent: QWidget | None):
        msgbox = QMessageBox(parent)
        msgbox.setWindowTitle("Critical Error")
        msgbox.setText(text)
        msgbox.setIcon(QMessageBox.Icon.Critical)
        msgbox.exec()
