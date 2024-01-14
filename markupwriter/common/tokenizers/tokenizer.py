#!/usr/bin/python

import re

from PyQt6.QtCore import (
    QObject,
    QRunnable,
    pyqtSignal,
    pyqtSlot,
)


class WorkerSignal(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(str)
    result = pyqtSignal(str, list)


class Tokenizer(QRunnable):
    def __init__(self, uuid: str, text: str, parent: QObject | None) -> None:
        super().__init__()
        self.uuid = uuid
        self.text = text
        self.signals = WorkerSignal(parent)
        self.pattern = re.compile(r"^@(create|import)")

    @pyqtSlot()
    def run(self):
        try:
            tokens: list[list[str]] = list()

            index = self.text.find("\n")
            while index > -1:
                line = self.text[: index + 1].strip()
                self.text = self.text[index + 1 :]
                index = self.text.find("\n")

                found = self.pattern.search(line)
                if found is None:
                    continue
                
                tokens.append(line.split(" "))

        except Exception as e:
            self.signals.error.emit(str(e))

        else:
            self.signals.finished.emit()
            self.signals.result.emit(self.uuid, tokens)
