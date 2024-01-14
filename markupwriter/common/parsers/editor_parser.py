#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    QRunnable,
    pyqtSignal,
    pyqtSlot,
)

from markupwriter.common.referencetag import (
    RefTagManager,
)


class WorkerSignal(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(str)
    result = pyqtSignal()


class EditorParser(QRunnable):
    def __init__(
        self,
        uuid: str,
        tokens: dict[str, list[str]],
        refManager: RefTagManager,
        parent: QObject | None,
    ) -> None:
        super().__init__()
        self.uuid = uuid
        self.tokens = tokens
        self.refManager = refManager
        self.signals = WorkerSignal(parent)

    @pyqtSlot()
    def run(self):
        try:
            func: dict[str, function] = {
                "@create": self._handleCreateTag,
                "@import": self._handleImportTag,
            }

            for key in self.tokens:
                for t in self.tokens[key]:
                    func[key](t)

        except Exception as e:
            self.signals.error.emit(str(e))

        else:
            self.signals.finished.emit()
            self.signals.result.emit()

    def _handleCreateTag(self, names: list[str]):
        print(names)

    def _handleImportTag(self, names: list[str]):
        print(names)
