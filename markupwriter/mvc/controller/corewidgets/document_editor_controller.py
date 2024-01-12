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

from markupwriter.config import AppConfig
from markupwriter.common.util import File


class DocumentEditorController(QObject):
    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)

        self.model = DocumentEditor(self)
        self.view = DocumentEditorView(None)
        
    def setup(self):
        pass
    
    @pyqtSlot(str, list)
    def onFileAdded(self, uuid: str, path: list[str]):
        if self._isIdMatching(uuid):
            return
        self._writeCurrentFile()
        self.model.currDocPath = self._makePathStr(path)
        self.model.currDocUUID = uuid
        self._readCurrentFile()
        self.view.setPathLabel(self.model.currDocPath)
    
    @pyqtSlot(str)
    def onFileRemoved(self, uuid: str):
        if not self._isIdMatching(uuid):
            return
        self.model.currDocPath = ""
        self.model.currDocUUID = ""
        self.view.clearAll()
    
    @pyqtSlot(str, list)
    def onFileMoved(self, uuid: str, path: list[str]):
        if not self._isIdMatching(uuid):
            return
        self.model.currDocPath = self._makePathStr(path)
        self.view.setPathLabel(self.model.currDocPath)
    
    @pyqtSlot(str, list)
    def onFileDoubleClicked(self, uuid: str, path: list[str]):
        self.onFileAdded(uuid, path)
    
    def _isIdMatching(self, uuid: str) -> bool:
        return self.model.currDocUUID == uuid
    
    def _writeCurrentFile(self):
        if self.model.currDocUUID == "":
            return
        path = AppConfig.projectContentPath()
        if path is None:
            return
        path += self.model.currDocUUID
        File.write(path, self.view.textEdit.toPlainText())
    
    def _readCurrentFile(self):
        if self.model.currDocUUID == "":
            return
        path = AppConfig.projectContentPath()
        if path is None:
            return
        path += self.model.currDocUUID
        content = File.read(path)
        self.view.textEdit.setPlainText(content)
        
    def _makePathStr(self, pathList: list[str]) -> str:
        text = ""
        count = len(pathList)
        for i in range(count-1):
            text += "{} \u203a ".format(pathList[i])
        
        text += "{}".format(pathList[count-1])
        
        return text
        
    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        self._writeCurrentFile()
        return sout
    
    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        return sin
