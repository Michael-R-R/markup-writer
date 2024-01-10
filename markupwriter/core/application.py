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

from markupwriter.controller.core import (
    MainWindowController,
)


class Application(object):
    status = -1
    controller: MainWindowController = None

    def start():
        AppConfig.init()
        HighlighterConfig.init()
        HotkeyConfig.init()
        SerializeConfig.read()

    def run(argv: list[str]):
        app = QApplication(argv)
        app.setApplicationName(AppConfig.APP_NAME)

        Application.controller = MainWindowController(None)
        Application.controller.setup()
        Application.controller.show()

        Application.status = app.exec()

    def close():
        SerializeConfig.write()
