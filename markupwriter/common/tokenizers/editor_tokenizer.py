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
    result = pyqtSignal(str, dict)


class EditorTokenizer(QRunnable):
    def __init__(self, uuid: str, text: str, parent: QObject | None) -> None:
        super().__init__()
        self.uuid = uuid
        self.text = text
        self.signals = WorkerSignal(parent)
        self.tagPattern = re.compile(r"^@(tag).*", re.MULTILINE)
        self.namesPattern = re.compile(r"(?<=\[).+?(?=\])")

    @pyqtSlot()
    def run(self):
        try:
            tokens: dict[str, list[str]] = {
                "@tag": list(),
            }

            it = self.tagPattern.finditer(self.text)
            for found in it:
                line = found.group(0)
                namesFound = self.namesPattern.search(line)
                if namesFound is None:
                    continue
                
                names = namesFound.group(0)
                nameList = [n.strip() for n in names.split(",")]
                
                tokens["@tag"].append(nameList)

        except Exception as e:
            self.signals.error.emit(str(e))

        else:
            self.signals.finished.emit()
            self.signals.result.emit(self.uuid, tokens)
