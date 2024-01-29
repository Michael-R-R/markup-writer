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
        # --- Editor bar --- #
        editorBar = self.view.editorBar
        editorBar.closeAction.triggered.connect(self._onCloseDocument)

        # --- Text edit --- #
        textEdit = self.view.textEdit
        textEdit.searchAction.triggered.connect(self._onToggleSearchBox)
        textEdit.tagHovered.connect(self._onTagHovered)

        # --- Search widget --- #
        searchWidget = self.view.searchWidget

    def reset(self):
        self.model.currDocPath = ""
        self.model.currDocUUID = ""
        self.view.reset()
        self.hasOpenDocument.emit(False)

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

        info: (int, str) = self.readDoc(uuid)
        if info == (None, None):
            self.onFileRemoved(uuid)
            return

        self.view.editorBar.addPath(self.model.currDocPath)
        self.view.editorBar.addCloseAction()
        self.view.textEdit.setPlainText(info[1])
        self.view.textEdit.moveCursorTo(info[0])
        self.view.textEdit.setEnabled(True)
        self.view.textEdit.setFocus()

        self.runTokenizer(uuid)
        
        searchWidget = self.view.searchWidget
        if searchWidget.isVisible():
            searchWidget.runSearch()

        self.hasOpenDocument.emit(True)

    def onFileRemoved(self, uuid: str):
        self.model.parser.popPrevUUID(uuid, self.model.refManager)
        if not self._hasMatchingID(uuid):
            return
        self.reset()

    def onFileMoved(self, uuid: str, path: list[str]):
        if not self._hasMatchingID(uuid):
            return
        self.model.currDocPath = self._makePathStr(path)
        self.view.editorBar.addPath(self.model.currDocPath)

    def onFileRenamed(self, uuid: str, old: str, new: str):
        if not self._hasMatchingID(uuid):
            return
        self.model.currDocPath = self.model.currDocPath.replace(old, new)
        self.view.editorBar.addPath(self.model.currDocPath)

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

        textedit = self.view.textEdit
        content = "cpos:{}\n".format(textedit.textCursor().position())
        content += textedit.toPlainText()

        path = os.path.join(path, uuid)
        if not File.write(path, content):
            return False

        self.runWordCounter()

        return True

    def readDoc(self, uuid: str) -> (int | None, str | None):
        if not self._hasDocument():
            return (None, None)

        path = AppConfig.projectContentPath()
        if path is None:
            return (None, None)

        path = os.path.join(path, uuid)
        content = File.read(path)
        if content is None:
            return (None, None)

        cpos = 0
        found = re.search(r"^cpos:.+", content)
        if found is not None:
            cpos = int(found.group(0)[5:])
            content = content[found.end() + 1 :]

        return (cpos, content)

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

    @pyqtSlot()
    def _onCloseDocument(self):
        self.onSaveDocument()
        self.reset()

    @pyqtSlot()
    def _onToggleSearchBox(self):
        self.view.searchWidget.toggle()

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
