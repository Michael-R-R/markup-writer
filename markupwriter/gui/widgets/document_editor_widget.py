#!/usr/bin/python

import os, regex

from PyQt6.QtCore import (
    Qt,
    pyqtSignal,
    pyqtSlot,
    QPoint,
    QSize,
    QMimeData,
    QDataStream,
)

from PyQt6.QtGui import (
    QKeyEvent,
    QMouseEvent,
    QResizeEvent,
    QTextOption,
    QTextCursor,
    QAction,
    QKeySequence,
)

from PyQt6.QtWidgets import (
    QPlainTextEdit,
    QWidget,
    QFrame,
)

from markupwriter.config import ProjectConfig
from markupwriter.common.syntax import Highlighter, BEHAVIOUR
from markupwriter.common.referencetag import RefTagManager
from markupwriter.common.parsers import EditorParser
from markupwriter.common.util import File, Regex

import markupwriter.support.doceditor as de
import markupwriter.support.doceditor.state as s


class DocumentEditorWidget(QPlainTextEdit):
    stateChanged = pyqtSignal(str)
    stateBufferChanged = pyqtSignal(str)
    docStatusChanged = pyqtSignal(bool)
    showRefPopupClicked = pyqtSignal(QPoint)
    showRefTagClicked = pyqtSignal(QPoint)
    wordCountChanged = pyqtSignal(str, int)
    resized = pyqtSignal(QSize)

    def __init__(self, parent: QWidget | None):
        super().__init__(parent)

        self.state: s.BaseEditorState = None
        self.plainDocument = de.PlainDocument(self)
        self.spellChecker = de.SpellCheck()
        self.refManager = RefTagManager()
        self.highlighter = Highlighter(self.plainDocument, self.refManager, self.spellChecker.endict)
        self.parser = EditorParser()
        self.searchHotkey = QAction("search", self)
        self.canResizeMargins = True
        self.docUUID = ""
        self.isDirty = False

        shortcut = QKeySequence(Qt.Modifier.CTRL | Qt.Key.Key_F)
        self.searchHotkey.setShortcut(shortcut)
        self.addAction(self.searchHotkey)

        self.plainDocument.setDocumentMargin(12)

        self.setDocument(self.plainDocument)
        self.setEnabled(False)
        self.setMouseTracking(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setWordWrapMode(QTextOption.WrapMode.WordWrap)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.setTabStopDistance(20.0)

        self.setState(s.NormalEditorState(self, self))

        self.plainDocument.contentsChange.connect(self.contentsChangeUpdated)
        self.cursorPositionChanged.connect(self.cursorPosUpdated)
        self.modificationChanged.connect(self.modificationsUpdated)

    def reset(self):
        self.clear()
        self.setEnabled(False)
        self.docUUID = ""
        self.isDirty = False
        self.docStatusChanged.emit(False)
        
    def read(self, uuid: str, path: str) -> bool:
        if uuid == "":
            return False,
        
        text = File.read(path)
        if text is None:
            return False
            
        self.setText(uuid, text)

        self.isDirty = False
        
        return True
        
    def write(self, path: str) -> bool:
        if not self.hasOpenDocument():
            print("No document opened. Will not save...")
            return False

        if not self.isDirty:
            print("No changes made to document. Will not save...")
            return False
        
        cpos = self.textCursor().position()

        currentText = self.toPlainText()

        configText = "[CONFIG]\n"
        configText += f"cpos:{cpos}\n"
        configText += "[CONFIG END]\n"

        text = configText + currentText

        self.isDirty = False

        print("Saving document...")
        
        return File.write(path, text)
    
    def checkWordCount(self):
        if not self.hasOpenDocument():
            return
        
        lExclude = r"tag|ref|plot|tl|char|loc|obj|img|title|chapter|scene|section"
        rExclude = r"i|b|alignl|alignc|alignr"
        findRegex = r"\b(?<!@({})(?:\([^)]*)?)(?<!@)(?!({})\b)\w+\b".format(lExclude, rExclude)
        
        found = regex.findall(findRegex, self.toPlainText())
        count = len(found)
        
        self.wordCountChanged.emit(self.docUUID, count)

    def cursorToEnd(self):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.setTextCursor(cursor)
        self.centerCursor()

    def moveCursorTo(self, pos: int):
        cursor = self.textCursor()
        cursor.setPosition(pos)
        self.setTextCursor(cursor)
        self.centerCursor()
    
    def hasOpenDocument(self) -> bool:
        return self.docUUID != ""
        
    def setText(self, uuid: str, text: str):
        if uuid == "":
            self.reset()
            return
        
        cpos = 0
        configText = Regex.getDocumentConfig(text)
        if configText is not None:
            cpos = Regex.getCPos(configText)
            text = Regex.getDocumentText(text)
        
        self.docUUID = uuid
        self.setPlainText(text)
        self.moveCursorTo(cpos)
        self.setEnabled(True)
        self.docStatusChanged.emit(True)
    
    def setState(self, state: s.BaseEditorState):
        if self.state is not None:
            self.state.exit()
        
        self.state = state
        self.state.enter()
        
        self.state.changedState.connect(self.onChangedState)
        
    def findTagAtPos(self, pos: QPoint) -> str | None:
        cursor = self.cursorForPosition(pos)
        cpos = cursor.positionInBlock()
        textBlock = cursor.block().text()
        if cpos <= 0 or cpos >= len(textBlock):
            return None

        found = regex.search(r"@(ref|plot|tl|char|loc|obj)(\(.*\))", textBlock)
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
        
    def findRefUUID(self, refTag: str) -> str | None:
        return self.refManager.findUUID(refTag)
        
    def popParserUUID(self, uuid: str):
        self.parser.popPrevUUID(uuid, self.refManager)
        
    @pyqtSlot(int, int, int)
    def contentsChangeUpdated(self, pos: int, removed: int, added: int):
        print("Updating dirty document(contents changed):", (removed > 0 or added > 0))
        self.isDirty = (removed > 0 or added > 0)
    
    @pyqtSlot()
    def cursorPosUpdated(self):
        print("Updating dirty document(text cursor moved):", True)
        self.isDirty = True

    @pyqtSlot(bool)
    def modificationsUpdated(self, dirty: bool):
        print("Updating dirty document(modifications updated):", dirty)
        self.isDirty = dirty

    @pyqtSlot(str, dict)
    def runParser(self, uuid: str, tokens: dict[str, list[str]]):
        self.parser.run(uuid, tokens, self.refManager)
        self.highlighter.rehighlight()
    
    @pyqtSlot(s.STATE)
    def onChangedState(self, state: s.STATE):
        match state:
            case s.STATE.normal:
                self.setState(s.NormalEditorState(self, self))
                self.stateChanged.emit("NORMAL")
            case s.STATE.insert:
                self.setState(s.InsertEditorState(self, self))
                self.stateChanged.emit("INSERT")
            case s.STATE.append:
                self.setState(s.InsertEditorState(self, self, True))
                self.stateChanged.emit("INSERT")
            case s.STATE.visual:
                self.setState(s.VisualEditorState(self, self))
                self.stateChanged.emit("VISUAL")

    def canInsertFromMimeData(self, source: QMimeData | None) -> bool:
        hasUrls = source.hasUrls()
        status = super().canInsertFromMimeData(source)

        return hasUrls or status

    def insertFromMimeData(self, source: QMimeData | None) -> None:
        if source.hasUrls():
            extRegex = regex.compile(r"\b\.(jpeg|jpg|png|gif)\b")
            for url in source.urls():
                imgPath = url.path()
                found = extRegex.search(imgPath)
                if found is None:
                    continue
                imgTag = "@img({})".format(imgPath)
                self.textCursor().insertText(imgTag)
        else:
            return super().insertFromMimeData(source)

    def resizeEvent(self, e: QResizeEvent | None) -> None:
        if self.canResizeMargins:
            self.canResizeMargins = False
            self.resized.emit(e.size())
            self.canResizeMargins = True
        
        return super().resizeEvent(e)

    def keyPressEvent(self, e: QKeyEvent | None) -> None:
        self._onChangeCursorShape(e.modifiers(), self.viewport())

        if self.state.process(e):
            self.stateBufferChanged.emit(self.state.buffer)
        else:
            super().keyPressEvent(e)

    def keyReleaseEvent(self, e: QKeyEvent | None) -> None:
        self._onChangeCursorShape(e.modifiers(), self.viewport())

        return super().keyReleaseEvent(e)

    def mousePressEvent(self, e: QMouseEvent | None) -> None:
        ctrl = Qt.KeyboardModifier.ControlModifier
        alt = Qt.KeyboardModifier.AltModifier
        button = Qt.MouseButton.LeftButton

        if e.modifiers() == ctrl:
            if e.button() == button:
                self.showRefPopupClicked.emit(e.pos())
                return None
        elif e.modifiers() == (ctrl | alt):
            if e.button() == button:
                self.showRefTagClicked.emit(e.pos())
                return None

        return super().mousePressEvent(e)

    def mouseMoveEvent(self, e: QMouseEvent | None) -> None:
        self._onChangeCursorShape(e.modifiers(), self.viewport())

        return super().mouseMoveEvent(e)

    def _onChangeCursorShape(self, mods: Qt.KeyboardModifier, vp: QWidget):
        ctrl = Qt.KeyboardModifier.ControlModifier
        alt = Qt.KeyboardModifier.AltModifier

        if mods == ctrl or mods == (ctrl | alt):
            vp.setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            vp.setCursor(Qt.CursorShape.IBeamCursor)

    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        sout << self.spellChecker
        sout.writeQString(self.docUUID)
        return sout

    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        sin >> self.spellChecker
        
        uuid = sin.readQString()
        if ProjectConfig.hasActiveProject():
            cpath = ProjectConfig.contentPath()
            path = os.path.join(cpath, uuid)
            self.read(uuid, path)
        
        return sin
