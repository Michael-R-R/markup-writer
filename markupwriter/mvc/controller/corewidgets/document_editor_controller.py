#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    QDataStream,
    pyqtSlot,
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

from markupwriter.common.parsers import (
    EditorParser,
)

from markupwriter.config import AppConfig
from markupwriter.common.util import File


class DocumentEditorController(QObject):
    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)

        self.model = DocumentEditor(self)
        self.view = DocumentEditorView(None)
        
    def setup(self):
        texteditor = self.view.textEdit
        self.model.setHighlighterDoc(texteditor.plainDocument)
    
    @pyqtSlot()
    def runTokenizer(self):
        uuid = self.model.currDocUUID
        text = self.view.textEdit.toPlainText()
        tokenizer = EditorTokenizer(uuid, text, self)
        tokenizer.signals.result.connect(self.runParser)
        self.model.threadPool.start(tokenizer)
        
    @pyqtSlot(str, dict)
    def runParser(self, uuid: str, tokens: dict[str, list[str]]):
        parser = EditorParser(uuid, tokens, self.model.refTagManager, self)
        self.model.threadPool.start(parser)
    
    @pyqtSlot(str, list)
    def onFileAdded(self, uuid: str, path: list[str]):
        if self._isIdMatching(uuid):
            return
        self.writeCurrentFile()
        self.model.currDocPath = self._makePathStr(path)
        self.model.currDocUUID = uuid
        content = self.readCurrentFile()
        self.view.textEdit.setPlainText(content)
        self.view.setPathLabel(self.model.currDocPath)
        self.view.textEdit.setEnabled(True)
        self.runTokenizer()
    
    @pyqtSlot(str)
    def onFileRemoved(self, uuid: str):
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
        for i in range(count-1):
            text += "{} \u203a ".format(pathList[i])
        
        text += "{}".format(pathList[count-1])
        
        return text
        
    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        return sout
    
    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        return sin
