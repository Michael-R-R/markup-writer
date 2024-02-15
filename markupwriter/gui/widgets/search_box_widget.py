#!/usr/bin/python

import re

from PyQt6.QtCore import (
    pyqtSignal,
    pyqtSlot,
    QSize,
)

from PyQt6.QtGui import (
    QAction,
)

from PyQt6.QtWidgets import (
    QWidget,
    QFrame,
    QGridLayout,
    QLineEdit,
    QLabel,
    QToolBar,
)

from markupwriter.common.provider import Icon


class SearchBoxWidget(QFrame):
    searchChanged = pyqtSignal(str, bool)

    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)

        self._index = 0
        self._found = list()

        self.setAutoFillBackground(True)
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Plain)

        self.searchInput = QLineEdit(self)
        self.searchInput.setPlaceholderText("Search")
        self.searchInput.setContentsMargins(0, 0, 0, 0)
        self.searchInput.setMaximumHeight(20)

        self.resultsLabel = QLabel("None", self)
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
        self.gLayout.setVerticalSpacing(2)
        self.gLayout.addWidget(self.searchInput, 0, 0)
        self.gLayout.addWidget(self.resultsLabel, 0, 1)
        self.gLayout.addWidget(self.searchToolbar, 0, 2)
        self.gLayout.addWidget(self.replaceInput, 1, 0)
        self.gLayout.addWidget(self.replaceToolbar, 1, 1)

        self.searchInput.textChanged.connect(self.onSearchChanged)

    def reset(self):
        self.hide()
        self.searchInput.clear()
        self.replaceInput.clear()
        self.resultsLabel.setText("None")
        self.prevAction.setEnabled(False)
        self.nextAction.setEnabled(False)
        self.replaceAction.setEnabled(False)
        self.replaceAllAction.setEnabled(False)
        self._index = 0
        self._found = list()

    def toggle(self) -> bool:
        if self.isVisible():
            self.hide()
        else:
            self.show()
            
        return self.isVisible()

    def adjustPos(self, vbw: int, ww: int, fw: int):
        if not self.isVisible():
            return

        srw = self.width()

        x = ww - vbw - srw - 2 * fw
        y = 2 * fw
        self.move(x, y)

    def foundCount(self) -> int:
        return len(self._found)

    def setFound(self, found: list[re.Match[str]]):
        self._found = found
        self._index = -1
        self._updateStatus()

    def runMatch(self, cpos: int, direction: int) -> re.Match[str] | None:
        if self.foundCount() <= 0:
            return None
        
        # First match, find closest to cursor
        if self._index < 0:
            for f in self._found:
                self._index += 1
                if f.start() > cpos:
                    break
        # Otherwise update the index by direction
        else:
            self._index = (self._index + direction) % self.foundCount()

        self._updateStatus()
        
        return self._found[self._index]

    @pyqtSlot(str)
    def onSearchChanged(self, text: str, doHighlighter: bool = True):
        if text == "":
            self.searchChanged.emit("", doHighlighter)
            return
        
        text = "\\b{}\\b".format(text)
        self.searchChanged.emit(text, doHighlighter)

    def _updateStatus(self):
        count = self.foundCount()

        index = "?" if self._index < 0 else self._index + 1
        text = "None" if count <= 0 else "{} of {}".format(index, count)
        isEnabled = count > 0

        self.resultsLabel.setText(text)
        self.prevAction.setEnabled(isEnabled)
        self.nextAction.setEnabled(isEnabled)
        self.replaceAction.setEnabled(isEnabled)
        self.replaceAllAction.setEnabled(isEnabled)
