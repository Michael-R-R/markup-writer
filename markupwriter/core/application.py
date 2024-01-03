#!/usr/bin/python

from PyQt6.QtWidgets import (
    QApplication,
)

from markupwriter.config import (
    AppConfig,
    HighlighterConfig,
    HotkeyConfig,
    SerializeConfig,
)

from .main_window import MainWindow

class Application(object):
    status = -1

    def start():
        AppConfig.init()
        HighlighterConfig.init()
        HotkeyConfig.init()
        SerializeConfig.read()

    def run(argv: list[str]):
        app = QApplication(argv)
        app.setApplicationName(AppConfig.APP_NAME)

        window = MainWindow()
        window.show()

        Application.status = app.exec()

    def close():
        SerializeConfig.write()