#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    pyqtSignal,
    pyqtSlot,
    QDataStream,
    QPoint,
)

from PyQt6.QtGui import (
    QCursor,
)

from markupwriter.mvc.model.corewidgets import (
    DocumentEditor,
)

from markupwriter.mvc.view.corewidgets import (
    DocumentEditorView,
)

from markupwriter.common.tokenizers import (
    EditorTokenizer,
)

from markupwriter.config import AppConfig
from markupwriter.common.util import File
from markupwriter.widgets import PreviewPopupWidget


class DocumentEditorController(QObject):
    requestedTextPreview = pyqtSignal(str)

    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)

        self.model = DocumentEditor(self)
        self.view = DocumentEditorView(None)

    def setup(self):
        self.view.textEdit.tagHovered.connect(self.onTagHovered)

    @pyqtSlot(str)
    def onTagHovered(self, tag: str):
        refTag = self.model.refManager.getTag(tag)
        if refTag is None:
            return
        pos = QCursor.pos()
        w = PreviewPopupWidget(refTag.docUUID(), self.view)
        w.previewButton.clicked.connect(
            lambda: self.requestedTextPreview.emit(refTag.docUUID())
        )
        size = w.sizeHint()
        x = pos.x() - int((size.width() / 2))
        y = pos.y() - int(size.height() / 1.25)
        w.move(QPoint(x, y))
        w.show()

    @pyqtSlot()
    def runTokenizer(self, uuid: str):
        text = self.view.textEdit.toPlainText()
        tokenizer = EditorTokenizer(uuid, text, self)
        tokenizer.signals.result.connect(self.runParser)
        self.model.threadPool.start(tokenizer)

    @pyqtSlot(str, dict)
    def runParser(self, uuid: str, tokens: dict[str, list[str]]):
        self.model.parser.run(uuid, tokens)

    @pyqtSlot(str, list)
    def onFileAdded(self, uuid: str, path: list[str]):
        if self._isIdMatching(uuid):
            return
        self.writeCurrentFile()
        self.runTokenizer(self.model.currDocUUID)
        self.model.currDocPath = self._makePathStr(path)
        self.model.currDocUUID = uuid
        content = self.readCurrentFile()
        self.view.textEdit.setPlainText(content)
        self.view.setPathLabel(self.model.currDocPath)
        self.view.textEdit.setEnabled(True)
        self.runTokenizer(uuid)

    @pyqtSlot(str)
    def onFileRemoved(self, uuid: str):
        self.model.parser.popPrevUUID(uuid)
        if not self._isIdMatching(uuid):
            return
        self.model.currDocPath = ""
        self.model.currDocUUID = ""
        self.view.clearAll()
        self.view.textEdit.setEnabled(False)

    @pyqtSlot(str, list)
    def onFileMoved(self, uuid: str, path: list[str]):
        if not self._isIdMatching(uuid):
            return
        self.model.currDocPath = self._makePathStr(path)
        self.view.setPathLabel(self.model.currDocPath)

    @pyqtSlot(str, list)
    def onFileDoubleClicked(self, uuid: str, path: list[str]):
        self.onFileAdded(uuid, path)

    @pyqtSlot(str, str, str)
    def onFileRenamed(self, uuid: str, old: str, new: str):
        if not self._isIdMatching(uuid):
            return
        self.model.currDocPath = self.model.currDocPath.replace(old, new)
        self.view.setPathLabel(self.model.currDocPath)

    def writeCurrentFile(self):
        if self.model.currDocUUID == "":
            return
        path = AppConfig.projectContentPath()
        if path is None:
            return
        path += self.model.currDocUUID
        File.write(path, self.view.textEdit.toPlainText())

    def readCurrentFile(self) -> str:
        if self.model.currDocUUID == "":
            return
        path = AppConfig.projectContentPath()
        if path is None:
            return
        path += self.model.currDocUUID
        return File.read(path)

    def _isIdMatching(self, uuid: str) -> bool:
        return self.model.currDocUUID == uuid

    def _makePathStr(self, pathList: list[str]) -> str:
        text = ""
        count = len(pathList)
        for i in range(count - 1):
            text += "{} \u203a ".format(pathList[i])

        text += "{}".format(pathList[count - 1])

        return text

    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        return sout

    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        return sin
