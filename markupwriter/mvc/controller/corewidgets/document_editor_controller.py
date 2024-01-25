#!/usr/bin/python

import re
import os

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
from markupwriter.widgets import PopupPreviewWidget


class DocumentEditorController(QObject):
    hasOpenDocument = pyqtSignal(bool)
    wcChanged = pyqtSignal(str, int)
    filePreviewed = pyqtSignal(str)

    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)

        self.model = DocumentEditor(self)
        self.view = DocumentEditorView(None)

    def setup(self):
        self.view.textEdit.tagHovered.connect(self._onTagHovered)

    def onSaveDocument(self) -> bool:
        uuid = self.model.currDocUUID
        status = self.writeDoc(uuid)
        if status:
            self.runTokenizer(uuid)

        return status

    def onFileOpened(self, uuid: str, pathList: list[str]):
        if self._hasMatchingID(uuid):
            return
        
        prevUUID = self.model.currDocUUID
        self.writeDoc(prevUUID)
        self.runTokenizer(prevUUID)
        
        self.model.currDocPath = self._makePathStr(pathList)
        self.model.currDocUUID = uuid
        
        content = self.readDoc(uuid)
        self.view.textEdit.setPlainText(content)
        self.view.textEdit.cursorToEnd()
        self.view.textEdit.setEnabled(True)
        self.view.setPathLabel(self.model.currDocPath)
        
        self.runTokenizer(uuid)

        self.hasOpenDocument.emit(True)

    def onFileRemoved(self, uuid: str):
        self.model.parser.popPrevUUID(uuid, self.model.refManager)
        if not self._hasMatchingID(uuid):
            return
        
        self.model.currDocPath = ""
        self.model.currDocUUID = ""
        self.view.clearAll()
        self.view.textEdit.setEnabled(False)

        self.hasOpenDocument.emit(False)

    def onFileMoved(self, uuid: str, path: list[str]):
        if not self._hasMatchingID(uuid):
            return
        self.model.currDocPath = self._makePathStr(path)
        self.view.setPathLabel(self.model.currDocPath)

    def onFileRenamed(self, uuid: str, old: str, new: str):
        if not self._hasMatchingID(uuid):
            return
        self.model.currDocPath = self.model.currDocPath.replace(old, new)
        self.view.setPathLabel(self.model.currDocPath)

    def runTokenizer(self, uuid: str):
        text = ""
        if self._hasMatchingID(uuid):
            text = self.view.textEdit.toPlainText()
        else:
            path = os.path.join(AppConfig.projectContentPath(), uuid)
            text = File.read(path)

        tokenizer = EditorTokenizer(uuid, text, self)
        tokenizer.signals.result.connect(self._onRunParser)
        self.model.threadPool.start(tokenizer)

    def runWordCounter(self):
        if not self._hasDocument():
            return
        uuid = self.model.currDocUUID
        text = self.view.textEdit.toPlainText()
        count = len(re.findall(r"[a-zA-Z'-]+", text))
        self.wcChanged.emit(uuid, count)

    def writeDoc(self, uuid: str) -> bool:
        if not self._hasDocument():
            return False

        path = AppConfig.projectContentPath()
        if path is None:
            return False

        path = os.path.join(path, uuid)
        if not File.write(path, self.view.textEdit.toPlainText()):
            return False

        self.runWordCounter()

        return True

    def readDoc(self, uuid: str) -> str | None:
        if not self._hasDocument():
            return None

        path = AppConfig.projectContentPath()
        if path is None:
            return None

        path = os.path.join(path, uuid)
        return File.read(path)

    def _hasMatchingID(self, uuid: str) -> bool:
        return self.model.currDocUUID == uuid

    def _hasDocument(self) -> bool:
        return self.model.currDocUUID != ""

    def _makePathStr(self, pathList: list[str]) -> str:
        text = ""
        count = len(pathList)
        for i in range(count - 1):
            text += "{} \u203a ".format(pathList[i])

        text += "{}".format(pathList[count - 1])

        return text

    @pyqtSlot(str)
    def _onTagHovered(self, tag: str):
        refTag = self.model.refManager.getTag(tag)
        if refTag is None:
            return

        uuid = refTag.docUUID()

        w = PopupPreviewWidget(uuid, self.view)
        w.previewButton.clicked.connect(lambda: self.filePreviewed.emit(uuid))

        size = w.sizeHint()
        pos = QCursor.pos()
        x = pos.x() - int((size.width() / 2))
        y = pos.y() - int(size.height() / 1.25)

        w.move(QPoint(x, y))
        w.show()

    @pyqtSlot(str, dict)
    def _onRunParser(self, uuid: str, tokens: dict[str, list[str]]):
        self.model.parser.run(uuid, tokens, self.model.refManager)

    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        return sout

    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        return sin
