#!/usr/bin/python

from PyQt6.QtWidgets import (
    QMessageBox,
)


class YesNoDialog(object):
    def run(text: str) -> bool:
        box = QMessageBox()
        box.setText(text)
        box.setStandardButtons(
            QMessageBox.StandardButton.No | QMessageBox.StandardButton.Yes
        )
        box.setDefaultButton(QMessageBox.StandardButton.No)
        match box.exec():
            case QMessageBox.StandardButton.No:
                return False
            case QMessageBox.StandardButton.Yes:
                return True
            case _:
                return False
