#!/usr/bin/python

import sys

from PyQt6.QtWidgets import (
    QApplication,
)

from markupwriter.config import (
    readConfig,
    writeConfig,
    AppConfig
)

from .main_window import MainWindow

def run(argv: list[str]):
    readConfig()

    app = QApplication(argv)
    app.setApplicationName(AppConfig.APP_NAME)

    window = MainWindow()
    window.show()

    syscode = app.exec()

    writeConfig()

    sys.exit(syscode)