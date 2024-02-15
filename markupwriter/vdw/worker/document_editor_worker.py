#!/usr/bin/python

import os, re

from PyQt6.QtCore import (
    QObject,
    pyqtSlot,
    QSize,
    QThreadPool
)

from PyQt6.QtGui import (
    QGuiApplication,
)

from markupwriter.config import ProjectConfig
from markupwriter.common.util import File
from markupwriter.common.tokenizers import EditorTokenizer
from markupwriter.common.parsers import EditorParser
from markupwriter.common.referencetag import RefTagManager

import markupwriter.vdw.delegate as d


class DocumentEditorWorker(QObject):
    def __init__(self, ded: d.DocumentEditorDelegate, parent: QObject | None) -> None:
        super().__init__(parent)
        
        self.ded = ded
        self.refManager = RefTagManager()
        self.parser = EditorParser()
        self.threadPool = QThreadPool(self)
        
    @pyqtSlot()
    def onCloseDocument(self):
        self.onSaveDocument()
        self._resetWidgets()
    
    @pyqtSlot()
    def onSaveDocument(self):
        status = self._writeToDisk()
        if not status:
            return
        self._runTokenizer()

    @pyqtSlot(str, list)
    def onFileOpened(self, uuid: str, paths: list[str]):
        te = self.ded.view.textEdit
        if te.docUUID == uuid:
            return
        
        self._writeToDisk()
        self._runTokenizer()
        
        if not self._readFromDisk(uuid):
            self.onFileRemoved("", uuid)
            return
        
        eb = self.ded.view.editorBar
        eb.addPath(paths)
        eb.addCloseAction()
        
        te.setFocus()
        self._runTokenizer()
        
        sb = self.ded.view.searchBox
        if sb.isVisible():
            text = sb.searchInput.text()
            sb.onSearchChanged(text)
    
    @pyqtSlot(str, str)
    def onFileRemoved(self, title: str, uuid: str):
        te = self.ded.view.textEdit
        self.parser.popPrevUUID(uuid, self.refManager)
        if te.docUUID != uuid:
            return
        self._resetWidgets()
    
    @pyqtSlot(str, list)
    def onFileMoved(self, uuid: str, paths: list[str]):
        te = self.ded.view.textEdit
        if te.docUUID != uuid:
            return
        eb = self.ded.view.editorBar
        eb.addPath(paths)
    
    @pyqtSlot(str, str, str)
    def onFileRenamed(self, uuid: str, old: str, new: str):
        te = self.ded.view.textEdit
        if te.docUUID != uuid:
            return
        eb = self.ded.view.editorBar
        eb.replaceInPath(old, new)
    
    @pyqtSlot(QSize)
    def onEditorResized(self, _: QSize):
        self._resizeMargins()
    
    def _resetWidgets(self):
        eb = self.ded.view.editorBar
        te = self.ded.view.textEdit
        
        eb.reset()
        te.reset()
    
    def _readFromDisk(self, uuid: str) -> bool:
        te = self.ded.view.textEdit
        path = ProjectConfig.contentPath()
        if path is None:
            te.reset()
            return False

        path = os.path.join(path, uuid)
        content = File.read(path)
        if content is None:
            return False

        cpos = 0
        found = re.search(r"^cpos:.+", content)
        if found is not None:
            cpos = int(found.group(0)[5:])
            content = content[found.end() + 1 :]
            
        te.setDocumentText(uuid, content, cpos)
        
        return True
    
    def _writeToDisk(self) -> bool:
        te = self.ded.view.textEdit
        if not te.hasDocument():
            return False

        path = ProjectConfig.contentPath()
        if path is None:
            return False

        content = "cpos:{}\n".format(te.textCursor().position())
        content += te.toPlainText()

        path = os.path.join(path, te.docUUID)
        if not File.write(path, content):
            return False

        te.runWordCount()

        return True
    
    def _resizeMargins(self):
        te = self.ded.view.textEdit
        
        mSize = QGuiApplication.primaryScreen().size()
        mW = mSize.width()

        wW = te.width()
        if wW > int(mW * 0.75):
            wW = int(wW * 0.3)
        elif wW > int(mW * 0.5):
            wW = int(wW * 0.2)
        else:
            wW = int(wW * 0.1)

        wH = int(te.height() * 0.1)

        te.setViewportMargins(wW, wH, wW, wH)
    
    def _runTokenizer(self):
        te = self.ded.view.textEdit
        if not te.hasDocument():
            return
        
        uuid = te.docUUID
        text = te.toPlainText()

        tokenizer = EditorTokenizer(uuid, text, self)
        tokenizer.signals.result.connect(self._runParser)
        self.threadPool.start(tokenizer)
        
    @pyqtSlot(str, dict)
    def _runParser(self, uuid: str, tokens: dict[str, list[str]]):
        self.parser.run(uuid, tokens, self.refManager)
    