#!/usr/bin/python

from PyQt6.QtWidgets import (
    QMessageBox,
    QWidget,
)


class InfoDialog(object):
    def run(text: str, parent: QWidget | None):
        msgbox = QMessageBox(parent)
        msgbox.setWindowTitle("Information")
        msgbox.setText(text)
        msgbox.setIcon(QMessageBox.Icon.Information)
        msgbox.exec()
        

class ErrorDialog(object):
    def run(text: str, parent: QWidget | None):
        msgbox = QMessageBox(parent)
        msgbox.setWindowTitle("Critical Error")
        msgbox.setText(text)
        msgbox.setIcon(QMessageBox.Icon.Critical)
        msgbox.exec()
