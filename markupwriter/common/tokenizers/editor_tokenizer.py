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

        lineRegex = r"^@(tag)(\(.*\))"
        tagRegex = r"^@(tag)"
        namesRegex = r"(?<=\().+?(?=\))"

        self.uuid = uuid
        self.text = text
        self.linePattern = re.compile(lineRegex, re.MULTILINE)
        self.tagPattern = re.compile(tagRegex)
        self.namesPattern = re.compile(namesRegex)
        self.tokens: dict[str, list[str]] = {
            "@tag": list(),
        }
        self.signals = WorkerSignal(parent)

    @pyqtSlot()
    def run(self):
        try:
            it = self.linePattern.finditer(self.text)
            for found in it:
                line = found.group(0)
                tag = self.tagPattern.search(line).group(0)
                names = self.namesPattern.search(line).group(0)

                nameList = [n.strip() for n in names.split(",")]

                self.tokens[tag].append(nameList)

        except Exception as e:
            self.signals.error.emit(str(e))

        else:
            self.signals.finished.emit()
            self.signals.result.emit(self.uuid, self.tokens)
