#!/usr/bin/python

import re

from PyQt6.QtCore import (
    pyqtSlot,
    QSize,
)

from PyQt6.QtGui import (
    QAction,
    QHideEvent,
    QShowEvent,
    QTextCursor,
)

from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QLineEdit,
    QLabel,
    QToolBar,
)

from markupwriter.common.provider import Icon
from markupwriter.common.syntax import BEHAVIOUR
from . import DocumentEditorWidget


class SearchReplaceWidget(QFrame):
    def __init__(self, textEdit: DocumentEditorWidget | None) -> None:
        super().__init__(textEdit)

        self.textEdit = textEdit
        self.index = 0
        self.found = list()

        self.setAutoFillBackground(True)
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Plain)

        self.searchInput = QLineEdit(self)
        self.searchInput.setPlaceholderText("Search")
        self.searchInput.setContentsMargins(0, 0, 0, 0)
        self.searchInput.setMaximumHeight(20)

        self.resultsLabel = QLabel("No results", self)
        self.resultsLabel.setContentsMargins(0, 0, 0, 0)
        self.resultsLabel.setMaximumHeight(20)

        self.searchToolbar = QToolBar(self)
        self.searchToolbar.setIconSize(QSize(12, 12))
        self.searchToolbar.setContentsMargins(0, 0, 0, 0)
        self.prevAction = QAction(Icon.UP_ARROW, "Previous match", self)
        self.nextAction = QAction(Icon.DOWN_ARROW, "Next match", self)
        self.closeAction = QAction(Icon.UNCHECK, "Close", self)
        self.searchToolbar.addAction(self.prevAction)
        self.searchToolbar.addAction(self.nextAction)
        self.searchToolbar.addAction(self.closeAction)

        self.replaceInput = QLineEdit(self)
        self.replaceInput.setPlaceholderText("Replace")
        self.replaceInput.setContentsMargins(0, 0, 0, 0)
        self.replaceInput.setMaximumHeight(20)

        self.replaceToolbar = QToolBar(self)
        self.replaceToolbar.setIconSize(QSize(12, 12))
        self.replaceToolbar.setContentsMargins(0, 0, 0, 0)
        self.replaceAction = QAction(Icon.PLACE_HOLDER, "Replace", self)
        self.replaceAllAction = QAction(Icon.PLACE_HOLDER, "Replace all", self)
        self.replaceToolbar.addAction(self.replaceAction)
        self.replaceToolbar.addAction(self.replaceAllAction)

        self.gLayout = QGridLayout(self)
        self.gLayout.setVerticalSpacing(0)
        self.gLayout.addWidget(self.searchInput, 0, 0)
        self.gLayout.addWidget(self.resultsLabel, 0, 1)
        self.gLayout.addWidget(self.searchToolbar, 0, 2)
        self.gLayout.addWidget(self.replaceInput, 1, 0)
        self.gLayout.addWidget(self.replaceToolbar, 1, 1)

        self.searchInput.textChanged.connect(self.runSearch)
        self.prevAction.triggered.connect(self._onPrevMatch)
        self.nextAction.triggered.connect(self._onNextMatch)
        self.replaceAction.triggered.connect(self._onReplaceMatch)
        self.replaceAllAction.triggered.connect(self._onReplaceAllMatch)
        self.closeAction.triggered.connect(lambda: self.hide())

    def reset(self):
        self.hide()
        self.searchInput.clear()
        self.replaceInput.clear()
        self.resultsLabel.setText("None")
        self._setSearchActionStates(False)
        self._setReplaceActionStates(False)
        self._clearHighlighting()
        self.index = 0
        self.found = list()

    def toggle(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()

    def adjustPos(self):
        if not self.isVisible():
            return

        vb = self.textEdit.verticalScrollBar()
        vbw = vb.width() if vb.isVisible() else 0
        ww = self.textEdit.width()
        fw = self.textEdit.frameWidth()
        srw = self.width()

        x = ww - vbw - srw - 2 * fw
        y = 2 * fw
        self.move(x, y)

    @pyqtSlot()
    def runSearch(self):
        searchText = self.searchInput.text()
        if searchText == "":
            self.found = list()
            self.index = -1
            self._updateStates()
            self._clearHighlighting()
            return
        
        prevLength = len(self.found)
            
        content = self.textEdit.toPlainText()
        self.found = list(re.finditer(searchText, content, re.MULTILINE))
        self.index = -1
        
        if len(self.found) > 0:
            highlighter = self.textEdit.highlighter
            behaviour = highlighter.getBehaviour(BEHAVIOUR.searchword)
            behaviour.clear()
            behaviour.add(searchText)
            highlighter.rehighlight()
        elif prevLength > 0:
            self._clearHighlighting()
        
        self._updateStates()
        
    @pyqtSlot()
    def _onNextMatch(self):
        self._runMatch(1)

    @pyqtSlot()
    def _onPrevMatch(self):
        self._runMatch(-1)

    @pyqtSlot()
    def _onReplaceMatch(self):
        if self.index < 0:
            self._onNextMatch()
        else:
            self._selectText()
        
        replaceText = self.replaceInput.text()
        
        cursor = self.textEdit.textCursor()
        cursor.beginEditBlock()
        cursor.removeSelectedText()
        cursor.insertText(replaceText)
        cursor.endEditBlock()
        self.textEdit.setTextCursor(cursor)

        searchText = self.searchInput.text()
        content = self.textEdit.toPlainText()
        self.found = list(re.finditer(searchText, content, re.MULTILINE))
        if len(self.found) > 0:
            self._runMatch(0)
        else:
            self._updateStates()

    @pyqtSlot()
    def _onReplaceAllMatch(self):
        replaceText = self.replaceInput.text()
        searchText = self.searchInput.text()

        doc = self.textEdit.document()
        cursor = self.textEdit.textCursor()
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
        self.textEdit.setTextCursor(prevCursor)

        self.index = -1
        self.found = list()
        self._updateStates()

    def _runMatch(self, direction: int):
        # Find closet match to cursor
        if self.index < 0:
            cpos = self.textEdit.textCursor().position()
            for f in self.found:
                self.index += 1
                if f.start() > cpos:
                    break
        # Otherwise update the index(+-)
        else:
            self.index = (self.index + direction) % len(self.found)
            
        self._selectText()
        self._updateStates()

    def _selectText(self):
        if self.index < 0:
            return
        
        found = self.found[self.index]
        
        cursor = self.textEdit.textCursor()
        cursor.setPosition(found.start())
        cursor.setPosition(found.end(), QTextCursor.MoveMode.KeepAnchor)
        self.textEdit.setTextCursor(cursor)

    def _updateStates(self):
        count = len(self.found)
        
        index = "?" if self.index < 0 else self.index+1
        text = "None" if count <= 0 else "{} of {}".format(index, count)
        self.resultsLabel.setText(text)

        isEnabled = count > 0
        self._setSearchActionStates(isEnabled)
        self._setReplaceActionStates(isEnabled)

    def _setSearchActionStates(self, isEnabled: bool):
        self.prevAction.setEnabled(isEnabled)
        self.nextAction.setEnabled(isEnabled)

    def _setReplaceActionStates(self, isEnabled: bool):
        self.replaceAction.setEnabled(isEnabled)
        self.replaceAllAction.setEnabled(isEnabled)

    def _clearHighlighting(self):
        highlighter = self.textEdit.highlighter
        behaviour = highlighter.getBehaviour(BEHAVIOUR.searchword)
        behaviour.clear()
        highlighter.rehighlight()

    def showEvent(self, a0: QShowEvent | None) -> None:
        self.adjustPos()
        self.searchInput.setFocus()
        self.runSearch()
        return super().showEvent(a0)
    
    def hideEvent(self, a0: QHideEvent | None) -> None:
        self._clearHighlighting()
        return super().hideEvent(a0)
