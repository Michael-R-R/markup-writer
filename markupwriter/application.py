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

from markupwriter.common.provider import (
    Icon,
    Style
)

from markupwriter.mvc.controller.core import (
    MainWindowController,
)


class Application(object):
    status = -1
    controller: MainWindowController = None

    def start(wd: str):
        AppConfig.init(wd)
        HighlighterConfig.init(wd)
        HotkeyConfig.init(wd)
        Icon.init(wd)
        Style.init(wd)
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
