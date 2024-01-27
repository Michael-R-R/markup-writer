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

        self.setAutoFillBackground(True)
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Plain)

        self.searchInput = QLineEdit(self)
        self.searchInput.setContentsMargins(0, 0, 0, 0)
        self.searchInput.setMaximumHeight(20)

        self.resultsLabel = QLabel("No results", self)
        self.resultsLabel.setContentsMargins(0, 0, 0, 0)
        self.resultsLabel.setMaximumHeight(20)

        self.searchToolbar = QToolBar(self)
        self.searchToolbar.setIconSize(QSize(12,12))
        self.searchToolbar.setContentsMargins(0, 0, 0, 0)
        self.prevAction = QAction(Icon.UP_ARROW, "Previous match", self)
        self.nextAction = QAction(Icon.DOWN_ARROW, "Next match", self)
        self.closeAction = QAction(Icon.UNCHECK, "Close", self)
        self.searchToolbar.addAction(self.prevAction)
        self.searchToolbar.addAction(self.nextAction)
        self.searchToolbar.addAction(self.closeAction)

        self.replaceInput = QLineEdit(self)
        self.replaceInput.setContentsMargins(0, 0, 0, 0)
        self.replaceInput.setMaximumHeight(20)

        self.replaceToolbar = QToolBar(self)
        self.replaceToolbar.setIconSize(QSize(12,12))
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
        self.closeAction.triggered.connect(lambda: self.hide())

    def reset(self):
        self.hide()
        self.searchInput.clear()
        self.replaceInput.clear()

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

    pyqtSlot()

    def _onSearchChanged(self, text: str):
        print(text)
        # TODO implement
