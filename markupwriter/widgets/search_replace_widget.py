#!/usr/bin/python

import re

from PyQt6.QtCore import (
    Qt,
    pyqtSignal,
    pyqtSlot,
    QSize,
)

from PyQt6.QtGui import (
    QAction,
    QTextCursor,
)

from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QLineEdit,
    QLabel,
    QToolBar,
    QPlainTextEdit,
)

from markupwriter.common.provider import Icon


class SearchReplaceWidget(QFrame):
    def __init__(self, textEdit: QPlainTextEdit | None) -> None:
        super().__init__(textEdit)

        self.textEdit = textEdit
        self.searchText = ""
        self.index = 0
        self.found = None
        self.count = -1

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

        self.searchInput.textChanged.connect(self._onSearchChanged)
        self.prevAction.triggered.connect(self._onPrevMatch)
        self.nextAction.triggered.connect(self._onNextMatch)
        self.closeAction.triggered.connect(lambda: self.hide())

    def reset(self, doHide: bool = True):
        if doHide:
            self.hide()
            
        self.searchInput.clear()
        self.replaceInput.clear()
        self.resultsLabel.setText("No results")
        
        self.searchText = ""
        self.index = 0
        self.found = None
        self.count = 0

    def toggle(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
            self.adjustPos()

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

    @pyqtSlot(str)
    def _onSearchChanged(self, searchText: str):
        if searchText == "":
            self.reset(False)
            return
        
        content = self.textEdit.toPlainText()
        self.searchText = searchText
        self.index = 0
        self.found = list(re.finditer("\\b{}\\b".format(searchText), content, re.MULTILINE))
        self.count = len(self.found)

        if self.count <= 0:
            self.resultsLabel.setText("No results")
        else:
            self._traverseSearch(0)
            
    @pyqtSlot()
    def _onNextMatch(self):
        self._traverseSearch(1)
        
    @pyqtSlot()
    def _onPrevMatch(self):
        self._traverseSearch(-1)
        
    @pyqtSlot(str)
    def _onReplaceChanged(self, replaceText: str):
        pass
    
    @pyqtSlot()
    def _onReplaceMatch(self):
        pass
    
    @pyqtSlot()
    def _onReplaceAllMatch(self):
        pass
        
    def _traverseSearch(self, direction: int):
        if self.count <= 0:
            return
        
        self.index = (self.index + direction) % self.count
        self._updateResultsLabel(self.index+1, self.count)
        found = self.found[self.index]
        
        cursor = self.textEdit.textCursor()
        cursor.setPosition(found.start())
        cursor.setPosition(found.end(), QTextCursor.MoveMode.KeepAnchor)
        self.textEdit.setTextCursor(cursor)
        
    def _updateResultsLabel(self, index: int, count: int):
        if count <= 0:
            self.resultsLabel.setText("No results") # dog
        else:
            self.resultsLabel.setText("{} of {}".format(index, count))