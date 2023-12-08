#!/usr/bin/python

import sys

from PyQt6.QtWidgets import (
    QApplication,
)

from markupwriter.config import (
    config_app,
)

from .main_window import (
    MainWindow,
)

def run(argv: list[str]):
    app = QApplication(argv)
    app.setApplicationName(config_app.APP_NAME)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())