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
    QTextCursor,
)

from markupwriter.mvc.model.corewidgets import DocumentEditor
from markupwriter.mvc.view.corewidgets import DocumentEditorView
from markupwriter.common.tokenizers import EditorTokenizer
from markupwriter.common.syntax import BEHAVIOUR
from markupwriter.config import ProjectConfig
from markupwriter.common.util import File
from markupwriter.gui.widgets import PopupPreviewWidget


class DocumentEditorController(QObject):
    hasOpenDocument = pyqtSignal(bool)
    wcChanged = pyqtSignal(str, int)
    filePreviewed = pyqtSignal(str)

    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)

        self.model = DocumentEditor(self)
        self.view = DocumentEditorView(None)

    def setup(self):
        # --- View signals --- #
        view = self.view
        view.searchAction.triggered.connect(self._onToggleSearchBox)

        # --- Editor bar signals--- #
        editorBar = self.view.editorBar
        editorBar.closeAction.triggered.connect(self._onCloseDocument)

        # --- Text edit signals --- #
        textEdit = self.view.textEdit
        textEdit.tagPopupRequested.connect(self._onTagPopupRequested)
        textEdit.tagPreviewRequested.connect(self._onTagPreviewRequested)

        # --- Search box signals --- #
        searchBox = self.view.searchBox
        searchBox.searchChanged.connect(self._runSearch)
        searchBox.nextAction.triggered.connect(self._onNextMatch)
        searchBox.prevAction.triggered.connect(self._onPrevMatch)
        searchBox.replaceAction.triggered.connect(self._onReplaceMatch)
        searchBox.replaceAllAction.triggered.connect(self._onReplaceAllMatch)
        searchBox.closeAction.triggered.connect(self._onToggleSearchBox)

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

        info: tuple[int, str] = self.readDoc(uuid)
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

        searchBox = self.view.searchBox
        if searchBox.isVisible():
            searchBox.onSearchChanged(searchBox.searchInput.text())

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
            path = os.path.join(ProjectConfig.contentPath(), uuid)
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

        path = ProjectConfig.contentPath()
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

    def readDoc(self, uuid: str) -> tuple[int | None, str | None]:
        if not self._hasDocument():
            return (None, None)

        path = ProjectConfig.contentPath()
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

    # ---- Document editor slots ---- #
    @pyqtSlot(str, int)
    def _onTagPopupRequested(self, blockText: str, pos: int):
        tag = self._parseTagFromBlock(blockText, pos)
        if tag is None:
            return
        
        uuid = self.model.refManager.findUUID(tag)
        if uuid is None:
            return

        w = PopupPreviewWidget(uuid, self.view)
        w.previewButton.clicked.connect(lambda: self.filePreviewed.emit(uuid))

        size = w.sizeHint()
        cpos = QCursor.pos()
        x = cpos.x() - int((size.width() / 2))
        y = cpos.y() - int(size.height() / 1.25)

        w.move(QPoint(x, y))
        w.show()
        
    @pyqtSlot(str, int)
    def _onTagPreviewRequested(self, blockText: str, pos: int):
        tag = self._parseTagFromBlock(blockText, pos)
        if tag is None:
            return
        
        uuid = self.model.refManager.findUUID(tag)
        if uuid is None:
            return

        self.filePreviewed.emit(uuid)
        
    def _parseTagFromBlock(self, blockText: str, pos: int) -> str | None:
        found = re.search(r"^@(ref|pov|loc)(\(.*\))", blockText)
        if found is None:
            return None
        
        rcomma = blockText.rfind(",", 0, pos)
        fcomma = blockText.find(",", pos)
        tag = None
        
        # single tag
        if rcomma < 0 and fcomma < 0:
            rindex = blockText.rfind("(", 0, pos)
            lindex = blockText.find(")", pos)
            tag = blockText[rindex + 1 : lindex].strip()
        # tag start
        elif rcomma < 0 and fcomma > -1:
            index = blockText.rfind("(", 0, pos)
            tag = blockText[index + 1 : fcomma].strip()
        # tag middle
        elif rcomma > -1 and fcomma > -1:
            tag = blockText[rcomma + 1 : fcomma].strip()
        # tag end
        elif rcomma > -1 and fcomma < 0:
            index = blockText.find(")", pos)
            tag = blockText[rcomma + 1 : index].strip()

        return tag

    @pyqtSlot(str, dict)
    def _onRunParser(self, uuid: str, tokens: dict[str, list[str]]):
        self.model.parser.run(uuid, tokens, self.model.refManager)

    # ---- Search replace slots ---- #
    @pyqtSlot()
    def _onToggleSearchBox(self):
        if not self._hasDocument():
            return

        searchBox = self.view.searchBox
        if searchBox.toggle():
            self.view.adjustSearchBoxPos()
            searchBox.searchInput.setFocus()
            searchBox.onSearchChanged(searchBox.searchInput.text())
        else:
            textEdit = self.view.textEdit
            highlighter = textEdit.highlighter
            behaviour = highlighter.getBehaviour(BEHAVIOUR.searchText)
            behaviour.clear()
            highlighter.rehighlight()

    @pyqtSlot(str, bool)
    def _runSearch(self, text: str, doHighlighter: bool = True):
        searchBox = self.view.searchBox
        textEdit = self.view.textEdit

        found = list()
        if text != "":
            content = textEdit.toPlainText()
            found = list(re.finditer(text, content, re.MULTILINE))

        if doHighlighter:
            highlighter = textEdit.highlighter
            behaviour = highlighter.getBehaviour(BEHAVIOUR.searchText)
            if len(found) > 0:
                behaviour.clear()
                behaviour.add(text)
                highlighter.rehighlight()
            elif searchBox.foundCount() > 0:
                behaviour.clear()
                highlighter.rehighlight()

        searchBox.setFound(found)

    @pyqtSlot()
    def _onNextMatch(self):
        self._onRunMatch(1)

    @pyqtSlot()
    def _onPrevMatch(self):
        self._onRunMatch(-1)

    @pyqtSlot()
    def _onReplaceMatch(self) -> bool:
        if not self._onRunMatch(0):
            return False

        searchBox = self.view.searchBox
        searchText = searchBox.searchInput.text()
        replaceText = searchBox.replaceInput.text()

        textEdit = self.view.textEdit
        cursor = textEdit.textCursor()
        cursor.beginEditBlock()
        cursor.removeSelectedText()
        cursor.insertText(replaceText)
        cursor.endEditBlock()
        textEdit.setTextCursor(cursor)

        searchBox.onSearchChanged(searchText, False)

        return self._onRunMatch(0)

    @pyqtSlot()
    def _onReplaceAllMatch(self):
        searchBox = self.view.searchBox
        textEdit = self.view.textEdit
        searchText = searchBox.searchInput.text()
        replaceText = searchBox.replaceInput.text()

        doc = textEdit.document()
        cursor = textEdit.textCursor()
        cursor.setPosition(0)
        cursor.beginEditBlock()

        prevCursor = doc.find(searchText, cursor)
        currCursor = prevCursor
        while not currCursor.isNull():
            prevCursor = currCursor
            currCursor.removeSelectedText()
            currCursor.insertText(replaceText)
            currCursor = doc.find(searchText, prevCursor)

        prevCursor.endEditBlock()
        textEdit.setTextCursor(prevCursor)

        searchBox.setFound(list())

    def _onRunMatch(self, direction: int) -> bool:
        searchBox = self.view.searchBox
        textEdit = self.view.textEdit
        cursor = textEdit.textCursor()
        cpos = cursor.position()

        found = searchBox.runMatch(cpos, direction)
        if found is None:
            return False

        cursor.setPosition(found.start())
        cursor.setPosition(found.end(), QTextCursor.MoveMode.KeepAnchor)
        textEdit.setTextCursor(cursor)

        return True

    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        return sout

    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        return sin
