#!/usr/bin/python

from PyQt6.QtCore import (
    pyqtSlot,
)

from PyQt6.QtWidgets import (
    QApplication,
)

from markupwriter.config import (
    AppConfig,
    HighlighterConfig,
    HotkeyConfig,
    SerializeConfig,
)

from markupwriter.coresupport.application import (
    SignalManager,
)

from .main_window import MainWindow


class Application(object):
    status = -1
    window: MainWindow = None

    def start():
        AppConfig.init()
        HighlighterConfig.init()
        HotkeyConfig.init()
        SerializeConfig.read()

    def run(argv: list[str]):
        app = QApplication(argv)
        app.setApplicationName(AppConfig.APP_NAME)

        Application.window = MainWindow()
        Application.window.show()
        Application._onSetupTriggered()
        Application.window.setupTriggered.connect(Application._onSetupTriggered)

        Application.status = app.exec()

    def close():
        SerializeConfig.write()

    @pyqtSlot()
    def _onSetupTriggered():
        SignalManager.setup(Application.window)
