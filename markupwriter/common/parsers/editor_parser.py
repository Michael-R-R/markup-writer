#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    QRunnable,
    pyqtSignal,
    pyqtSlot,
)


class WorkerSignal(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(str)
    result = pyqtSignal()


class EditorParser(QRunnable):
    def __init__(
        self, uuid: str, tokens: list[list[str]], parent: QObject | None
    ) -> None:
        super().__init__()
        self.uuid = uuid
        self.tokens = tokens
        self.signals = WorkerSignal(parent)

    @pyqtSlot()
    def run(self):
        try:
            pass
        
        except Exception as e:
            self.signals.error.emit(str(e))
        
        else:
            self.signals.finished.emit()
            self.signals.result.emit()
