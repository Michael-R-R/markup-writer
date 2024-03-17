#!/usr/bin/python

import os, re

from PyQt6.QtCore import (
    QObject,
    pyqtSignal,
    pyqtSlot,
    QSize,
    QThreadPool,
    QPoint,
)

from PyQt6.QtGui import (
    QGuiApplication,
    QTextCursor,
    QTextDocument,
    QCursor,
)

from markupwriter.config import ProjectConfig
from markupwriter.common.tokenizers import EditorTokenizer
from markupwriter.common.syntax import BEHAVIOUR
from markupwriter.gui.contextmenus.doceditor import EditorContextMenu
from markupwriter.gui.dialogs.modal import InfoDialog

import markupwriter.vdw.view as v
import markupwriter.gui.widgets as w


class DocumentEditorWorker(QObject):
    refPreviewRequested = pyqtSignal(str)
    
    def __init__(self, dev: v.DocumentEditorView, parent: QObject | None) -> None:
        super().__init__(parent)

        self.dev = dev
        self.threadPool = QThreadPool(self)
    
    @pyqtSlot()
    def onFocusEditorTriggered(self):
        te = self.dev.textEdit
        te.setFocus()
        
    @pyqtSlot(bool)
    def onHighlightToggled(self, status: bool):
        te = self.dev.textEdit
        highlighter = te.highlighter
        
        highlighter.toggleBehaviours()
        highlighter.rehighlight()
    
    @pyqtSlot(bool)
    def onSpellToggled(self, status: bool):
        te = self.dev.textEdit
        highlighter = te.highlighter
        
        highlighter.setBehaviourEnable(BEHAVIOUR.spellCheck, status)
        highlighter.rehighlight()
        
    @pyqtSlot(str)
    def onStateChanged(self, text: str):
        sb = self.dev.statusBar
        sb.normLabel.setText(text)
        
    @pyqtSlot(str)
    def onStateBufferChanged(self, text: str):
        sb = self.dev.statusBar
        sb.permLabel.setText(text)

    @pyqtSlot()
    def onCloseDocument(self):
        self.onSaveDocument()
        self._resetWidgets()

    @pyqtSlot()
    def onSaveDocument(self) -> bool:
        te = self.dev.textEdit
        
        cpath = ProjectConfig.contentPath()
        path = os.path.join(cpath, te.docUUID)
        if not te.write(path):
            return False

        te.checkWordCount()
        self._runTokenizer()

        return True

    @pyqtSlot(str, list)
    def onFileOpened(self, uuid: str, paths: list[str]):
        if uuid == "":
            return
        
        te = self.dev.textEdit
        if te.docUUID == uuid:
            return
        
        cpath = ProjectConfig.contentPath()
        
        path = os.path.join(cpath, te.docUUID)
        te.write(path)
        te.checkWordCount()
        self._runTokenizer()

        path = os.path.join(cpath, uuid)
        if not te.read(uuid, path):
            self.onFileRemoved("", uuid)
            return

        eb = self.dev.editorBar
        eb.addPath(self._buildPath(paths))

        self._runTokenizer()

        sb = self.dev.searchBox
        if sb.isVisible():
            text = sb.searchInput.text()
            sb.onSearchChanged(text)

    @pyqtSlot(str, str)
    def onFileRemoved(self, title: str, uuid: str):
        te = self.dev.textEdit
        te.popParserUUID(uuid)
        if te.docUUID != uuid:
            return
        self._resetWidgets()

    @pyqtSlot(str, list)
    def onFileMoved(self, uuid: str, paths: list[str]):
        te = self.dev.textEdit
        if te.docUUID != uuid:
            return
        eb = self.dev.editorBar
        eb.addPath(self._buildPath(paths))

    @pyqtSlot(str, str, str)
    def onFileRenamed(self, uuid: str, old: str, new: str):
        te = self.dev.textEdit
        if te.docUUID != uuid:
            return
        eb = self.dev.editorBar
        eb.replaceInPath(old, new)

    @pyqtSlot(QPoint)
    def onShowRefPopupClicked(self, pos: QPoint):
        te = self.dev.textEdit
        tag = te.findTagAtPos(pos)
        if tag is None:
            return

        te = self.dev.textEdit
        uuid = te.findRefUUID(tag)
        if uuid is None:
            InfoDialog.run("Tag does not exist", te)
            return

        popup = w.PopupPreviewWidget(uuid, te)
        popup.previewButton.clicked.connect(
            lambda: self.refPreviewRequested.emit(uuid)
        )

        size = popup.sizeHint()
        cpos = QCursor.pos()
        x = cpos.x() - int((size.width() / 2))
        y = cpos.y() - int(size.height() / 1.25)

        popup.move(QPoint(x, y))
        popup.show()

    @pyqtSlot(QPoint)
    def onShowRefPreviewClicked(self, pos: QPoint):
        te = self.dev.textEdit
        tag = te.findTagAtPos(pos)
        if tag is None:
            return

        te = self.dev.textEdit
        uuid = te.findRefUUID(tag)
        if uuid is None:
            InfoDialog.run("Tag does not exist", te)
            return

        self.refPreviewRequested.emit(uuid)

    @pyqtSlot(QSize)
    def onEditorResized(self, _: QSize):
        self._resizeMargins()

    @pyqtSlot(QPoint)
    def onContxtMenuRequested(self, pos: QPoint):
        te = self.dev.textEdit
        if te.isReadOnly():
            return

        sc = te.spellChecker
        h = te.highlighter
        contextMenu = EditorContextMenu(te, sc, h, pos, te)

        contextMenu.onShowMenu(te.mapToGlobal(pos))

    @pyqtSlot()
    def onSearchTriggered(self):
        te = self.dev.textEdit
        if not te.hasOpenDocument():
            return

        sb = self.dev.searchBox
        if sb.toggle():
            self.dev.adjustSearchBoxPos()
            sb.searchInput.setFocus()
            sb.onSearchChanged(sb.searchInput.text())
        else:
            highlighter = te.highlighter
            behaviour = highlighter.getBehaviour(BEHAVIOUR.searchText)
            behaviour.clear()
            highlighter.rehighlight()

    @pyqtSlot(str, bool)
    def onSearchChanged(self, text: str, doHighlight: bool):
        te = self.dev.textEdit
        sb = self.dev.searchBox

        found = list()
        if text != "":
            content = te.toPlainText()
            found = list(re.finditer(text, content, re.MULTILINE))

        if doHighlight:
            highlighter = te.highlighter
            behaviour = highlighter.getBehaviour(BEHAVIOUR.searchText)
            if len(found) > 0:
                behaviour.clear()
                behaviour.add(text)
                highlighter.rehighlight()
            elif sb.foundCount() > 0:
                behaviour.clear()
                highlighter.rehighlight()

        sb.setFound(found)

    @pyqtSlot()
    def onNextSearch(self):
        self._runSearch(1)

    @pyqtSlot()
    def onPrevSearch(self):
        self._runSearch(-1)

    @pyqtSlot()
    def onReplaceSearch(self):
        if not self._runSearch(0):
            return

        sb = self.dev.searchBox
        searchText = sb.searchInput.text()
        replaceText = sb.replaceInput.text()

        te = self.dev.textEdit
        cursor = te.textCursor()
        cursor.beginEditBlock()
        cursor.removeSelectedText()
        cursor.insertText(replaceText)
        cursor.endEditBlock()
        te.setTextCursor(cursor)

        sb.onSearchChanged(searchText, False)

        self._runSearch(0)

    @pyqtSlot()
    def onReplaceAllSearch(self):
        sb = self.dev.searchBox
        searchText = sb.searchInput.text()
        replaceText = sb.replaceInput.text()

        te = self.dev.textEdit
        doc = te.document()
        cursor = te.textCursor()
        cursor.setPosition(0)
        cursor.beginEditBlock()

        prevCursor = doc.find(searchText, cursor)
        currCursor = prevCursor
        while not currCursor.isNull():
            prevCursor = currCursor
            currCursor.removeSelectedText()
            currCursor.insertText(replaceText)
            currCursor = doc.find(
                searchText, prevCursor, QTextDocument.FindFlag.FindCaseSensitively
            )

        prevCursor.endEditBlock()
        te.setTextCursor(prevCursor)

        sb.setFound(list())

    def _resetWidgets(self):
        eb = self.dev.editorBar
        te = self.dev.textEdit

        eb.reset()
        te.reset()

    def _resizeMargins(self):
        te = self.dev.textEdit

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
        
    def _buildPath(self, paths: list[str]) -> str | None:
        count = len(paths)
        if count < 1:
            return None
        
        text = ""
        for i in range(count - 1):
            text += "{} \u203a ".format(paths[i])

        text += "{}".format(paths[count - 1])
        
        return text

    def _runTokenizer(self):
        te = self.dev.textEdit
        if not te.hasOpenDocument():
            return

        uuid = te.docUUID
        text = te.toPlainText()

        tokenizer = EditorTokenizer(uuid, text, self)
        tokenizer.signals.result.connect(te.runParser)
        self.threadPool.start(tokenizer)

    def _runSearch(self, direction: int) -> bool:
        te = self.dev.textEdit
        cursor = te.textCursor()
        cpos = cursor.position()

        sb = self.dev.searchBox
        found = sb.runMatch(cpos, direction)
        if found is None:
            return False

        cursor.setPosition(found.start())
        cursor.setPosition(found.end(), QTextCursor.MoveMode.KeepAnchor)
        te.setTextCursor(cursor)

        return True
