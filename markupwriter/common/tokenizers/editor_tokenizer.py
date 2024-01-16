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
        self.tagPattern = re.compile(r"^@(tag)")
        self.namesPattern = re.compile(r"(?<=\[).+?(?=\])")

    @pyqtSlot()
    def run(self):
        try:
            tokens: dict[str, list[str]] = {
                "@tag": list(),
            }

            index = self.text.find("\n")
            while index > -1:
                line = self.text[: index + 1].strip()
                self.text = self.text[index + 1 :]
                index = self.text.find("\n")

                tagFound = self.tagPattern.search(line)
                if tagFound is None:
                    continue
                
                namesFound = self.namesPattern.search(line)
                if namesFound is None:
                    return
                
                tag = tagFound.group(0)
                names = namesFound.group(0)
                
                nameList = [n.strip() for n in names.split(",")]
                    
                tokens[tag].append(nameList)

        except Exception as e:
            self.signals.error.emit(str(e))

        else:
            self.signals.finished.emit()
            self.signals.result.emit(self.uuid, tokens)
