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
            self._handlePrevTokens()
            self._handleCurrTokens()

        except Exception as e:
            self.signals.error.emit(str(e))

        else:
            self.signals.finished.emit()

    def _handlePrevTokens(self):
        pass
                
    def _handleCurrTokens(self):
        func: dict[str, function] = {
                "@tag": self._handleAddTag,
            }
        
        for key in self.tokens:
                for t in self.tokens[key]:
                    func[key](t)
        
    def _handleRemoveTag(self, names: list[str]):
        for n in names:
            self.refManager.removeTag(n)

    def _handleAddTag(self, names: list[str]):
        uuid = self.uuid
        for n in names:
            self.refManager.addTag(n, uuid)
