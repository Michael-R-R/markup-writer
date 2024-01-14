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
        self.keywordPattern = re.compile(r"^@(create|import)")
        self.sqbracketPattern = re.compile(r"(?<=\[).+(?=\])")

    @pyqtSlot()
    def run(self):
        try:
            tokens: dict[str, list[str]] = {
                "@create": list(),
                "@import": list(),
            }

            index = self.text.find("\n")
            while index > -1:
                line = self.text[: index + 1].strip()
                self.text = self.text[index + 1 :]
                index = self.text.find("\n")

                keywordFound = self.keywordPattern.search(line)
                if keywordFound is None:
                    continue
                
                namesFound = self.sqbracketPattern.search(line)
                if namesFound is None:
                    continue
                
                nameList = list()
                for n in namesFound.group(0).split(","):
                    nameList.append(n.strip())
                
                tokens[keywordFound.group(0)].append(nameList)

        except Exception as e:
            self.signals.error.emit(str(e))

        else:
            self.signals.finished.emit()
            self.signals.result.emit(self.uuid, tokens)
