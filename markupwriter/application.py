#!/usr/bin/python

from PyQt6.QtWidgets import (
    QApplication,
)

from markupwriter.config import (
    AppConfig,
    ProjectConfig,
    HighlighterConfig,
    HotkeyConfig,
    SerializeConfig,
)

from markupwriter.common.provider import (
    Icon,
    Style
)

import markupwriter.vdw as vdw


class Application(object):
    status = -1

    def start(wd: str):
        AppConfig.init(wd)
        ProjectConfig.init(wd)
        HighlighterConfig.init(wd)
        HotkeyConfig.init(wd)
        Icon.init(wd)
        Style.init(wd)
        SerializeConfig.read()

    def run(argv: list[str]):
        app = QApplication(argv)
        app.setApplicationName(AppConfig.APP_NAME)

        core = vdw.Core(app)
        core.run()

        Application.status = app.exec()

    def close():
        SerializeConfig.write()
