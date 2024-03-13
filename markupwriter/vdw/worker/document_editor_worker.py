#!/usr/bin/python

import os, re

from PyQt6.QtCore import (
    QObject,
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
from markupwriter.common.util import File
from markupwriter.common.tokenizers import EditorTokenizer
from markupwriter.common.parsers import EditorParser
from markupwriter.common.referencetag import RefTagManager
from markupwriter.common.syntax import BEHAVIOUR
from markupwriter.gui.contextmenus.doceditor import EditorContextMenu

import markupwriter.vdw.delegate as d
import markupwriter.gui.widgets as w


class DocumentEditorWorker(QObject):
    def __init__(self, ded: d.DocumentEditorDelegate, parent: QObject | None) -> None:
        super().__init__(parent)

        self.ded = ded
        self.refManager = RefTagManager()
        self.parser = EditorParser()
        self.threadPool = QThreadPool(self)

    def runWordCount(self, te: w.DocumentEditorWidget):
        if not te.hasOpenDocument():
            return

        uuid = te.docUUID
        text = te.toPlainText()
        count = len(re.findall(r"[a-zA-Z'-]+", text))

        te.wordCountChanged.emit(uuid, count)

    def findTagAtPos(self, pos: QPoint):
        te = self.ded.view.textEdit

        cursor = te.cursorForPosition(pos)
        cpos = cursor.positionInBlock()
        textBlock = cursor.block().text()
        if cpos <= 0 or cpos >= len(textBlock):
            return None

        found = re.search(r"@(ref|pov|loc)(\(.*\))", textBlock)
        if found is None:
            return None

        rcomma = textBlock.rfind(",", 0, cpos)
        fcomma = textBlock.find(",", cpos)
        tag = None

        # single tag
        if rcomma < 0 and fcomma < 0:
            rindex = textBlock.rfind("(", 0, cpos)
            lindex = textBlock.find(")", cpos)
            tag = textBlock[rindex + 1 : lindex].strip()
        # tag start
        elif rcomma < 0 and fcomma > -1:
            index = textBlock.rfind("(", 0, cpos)
            tag = textBlock[index + 1 : fcomma].strip()
        # tag middle
        elif rcomma > -1 and fcomma > -1:
            tag = textBlock[rcomma + 1 : fcomma].strip()
        # tag end
        elif rcomma > -1 and fcomma < 0:
            index = textBlock.find(")", cpos)
            tag = textBlock[rcomma + 1 : index].strip()

        return tag
    
    @pyqtSlot()
    def onFocusEditorTriggered(self):
        te = self.ded.view.textEdit
        te.setFocus()
    
    @pyqtSlot(bool)
    def onSpellToggled(self, isToggled: bool):
        te = self.ded.view.textEdit
        highlighter = te.highlighter
        
        highlighter.setBehaviourEnable(BEHAVIOUR.spellCheck, isToggled)
        highlighter.rehighlight()
        
    @pyqtSlot(str)
    def onStateChanged(self, text: str):
        sb = self.ded.view.statusBar
        sb.normLabel.setText(text)
        
    @pyqtSlot(str)
    def onStateBufferChanged(self, text: str):
        sb = self.ded.view.statusBar
        sb.permLabel.setText(text)

    @pyqtSlot()
    def onCloseDocument(self):
        self.onSaveDocument()
        self._resetWidgets()

    @pyqtSlot()
    def onSaveDocument(self) -> bool:
        status = self._writeToDisk()
        if not status:
            return False

        self._runTokenizer()

        return True

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

    @pyqtSlot(QPoint)
    def onShowRefPopupClicked(self, pos: QPoint):
        tag = self.findTagAtPos(pos)
        if tag is None:
            return

        uuid = self.refManager.findUUID(tag)
        if uuid is None:
            return

        popup = w.PopupPreviewWidget(uuid, self.ded.view)
        popup.previewButton.clicked.connect(
            lambda: self.ded.refPreviewRequested.emit(uuid)
        )

        size = popup.sizeHint()
        cpos = QCursor.pos()
        x = cpos.x() - int((size.width() / 2))
        y = cpos.y() - int(size.height() / 1.25)

        popup.move(QPoint(x, y))
        popup.show()

    @pyqtSlot(QPoint)
    def onShowRefPreviewClicked(self, pos: QPoint):
        tag = self.findTagAtPos(pos)
        if tag is None:
            return

        uuid = self.refManager.findUUID(tag)
        if uuid is None:
            return

        self.ded.refPreviewRequested.emit(uuid)

    @pyqtSlot(QSize)
    def onEditorResized(self, _: QSize):
        self._resizeMargins()

    @pyqtSlot(QPoint)
    def onContxtMenuRequested(self, pos: QPoint):
        te = self.ded.view.textEdit
        if te.isReadOnly():
            return

        sc = te.spellChecker
        h = te.highlighter
        contextMenu = EditorContextMenu(te, sc, h, pos, te)

        contextMenu.onShowMenu(te.mapToGlobal(pos))

    @pyqtSlot()
    def onSearchTriggered(self):
        te = self.ded.view.textEdit
        if not te.hasOpenDocument():
            return

        sb = self.ded.view.searchBox
        if sb.toggle():
            self.ded.view.adjustSearchBoxPos()
            sb.searchInput.setFocus()
            sb.onSearchChanged(sb.searchInput.text())
        else:
            highlighter = te.highlighter
            behaviour = highlighter.getBehaviour(BEHAVIOUR.searchText)
            behaviour.clear()
            highlighter.rehighlight()

    @pyqtSlot(str, bool)
    def onSearchChanged(self, text: str, doHighlight: bool):
        te = self.ded.view.textEdit
        sb = self.ded.view.searchBox

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

        sb = self.ded.view.searchBox
        searchText = sb.searchInput.text()
        replaceText = sb.replaceInput.text()

        te = self.ded.view.textEdit
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
        sb = self.ded.view.searchBox
        searchText = sb.searchInput.text()
        replaceText = sb.replaceInput.text()

        te = self.ded.view.textEdit
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
        if not te.hasOpenDocument():
            return False

        path = ProjectConfig.contentPath()
        if path is None:
            return False

        content = "cpos:{}\n".format(te.textCursor().position())
        content += te.toPlainText()

        path = os.path.join(path, te.docUUID)
        if not File.write(path, content):
            return False

        self.runWordCount(te)

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
        if not te.hasOpenDocument():
            return

        uuid = te.docUUID
        text = te.toPlainText()

        tokenizer = EditorTokenizer(uuid, text, self)
        tokenizer.signals.result.connect(self._runParser)
        self.threadPool.start(tokenizer)

    def _runSearch(self, direction: int) -> bool:
        te = self.ded.view.textEdit
        cursor = te.textCursor()
        cpos = cursor.position()

        sb = self.ded.view.searchBox
        found = sb.runMatch(cpos, direction)
        if found is None:
            return False

        cursor.setPosition(found.start())
        cursor.setPosition(found.end(), QTextCursor.MoveMode.KeepAnchor)
        te.setTextCursor(cursor)

        return True

    @pyqtSlot(str, dict)
    def _runParser(self, uuid: str, tokens: dict[str, list[str]]):
        self.parser.run(uuid, tokens, self.refManager)
