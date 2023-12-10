#!/usr/bin/python

from PyQt6.QtWidgets import (
    QApplication,
)

from markupwriter.config import (
    readConfig,
    writeConfig,
    AppConfig
)

from .main_window import MainWindow

def appStart():
    readConfig()

def appRun(argv: list[str]):
    app = QApplication(argv)
    app.setApplicationName(AppConfig.APP_NAME)

    window = MainWindow()
    window.show()

    return app.exec()

def appClose():
    writeConfig()