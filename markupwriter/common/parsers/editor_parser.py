#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    QRunnable,
    pyqtSignal,
    pyqtSlot,
)

from markupwriter.common.datastructure import (
    AST,
)


class WorkerSignal(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(str)
    result = pyqtSignal(str, AST)


class EditorParser(QRunnable):
    def __init__(
        self, uuid: str, tokens: list[list[str]], parent: QObject | None
    ) -> None:
        super().__init__()
        self.uuid = uuid
        self.tokens = tokens
        self.ast = AST(uuid)
        self.signals = WorkerSignal(parent)

    @pyqtSlot()
    def run(self):
        try:
            for t in self.tokens:
                self.ast.addAtExpression(t)
        
        except Exception as e:
            self.signals.error.emit(str(e))
        
        else:
            self.ast.prettyPrint(self.ast.root)
            self.signals.finished.emit()
            self.signals.result.emit(self.uuid, self.ast)
