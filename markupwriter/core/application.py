#!/usr/bin/python

from PyQt6.QtWidgets import (
    QApplication,
)

from markupwriter.config import (
    SerializeConfig,
    AppConfig
)

from .main_window import MainWindow

class Application(object):
    status = -1

    def start():
        SerializeConfig.read()

    def run(argv: list[str]):
        app = QApplication(argv)
        app.setApplicationName(AppConfig.APP_NAME)

        window = MainWindow()
        window.show()

        Application.status = app.exec()

    def close():
        SerializeConfig.write()