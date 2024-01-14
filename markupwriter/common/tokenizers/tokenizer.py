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
    result = pyqtSignal(dict)


class Tokenizer(QRunnable):
    def __init__(self, parent: QObject | None, text: str) -> None:
        super().__init__()
        self.text = text
        self.signals = WorkerSignal(parent)
        self.pattern = re.compile(r"^@(create|import)\s")

    @pyqtSlot()
    def run(self):
        try:
            tokens: dict[str, set[str]] = {
                "@create ": set(),
                "@import ": set(),
            }

            index = self.text.find("\n")
            while index > -1:
                line = self.text[: index + 1].strip()
                self.text = self.text[index + 1 :]
                index = self.text.find("\n")

                found = self.pattern.search(line)
                if found is None:
                    continue

                tokens[found.group(0)].add(line)

        except Exception as e:
            self.signals.error.emit(str(e))

        else:
            self.signals.finished.emit()
            self.signals.result.emit(tokens)
