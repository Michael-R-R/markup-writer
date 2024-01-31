#!/usr/bin/python

from PyQt6.QtCore import QEvent

from PyQt6.QtCore import (
    QSize,
)
from PyQt6.QtGui import QMouseEvent

from PyQt6.QtWidgets import (
    QWidget,
    QTabWidget,
    QTabBar,
)


class PreviewTabWidget(QTabWidget):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)

        self._prevIndex = -1

        self.setTabsClosable(True)
        self.setMovable(True)
        self.setContentsMargins(0, 0, 0, 0)
        self.setMouseTracking(True)

        self.currentChanged.connect(self._onCurrentChanged)

    def _onCurrentChanged(self, index: int):
        tabBar = self.tabBar()
        if tabBar is None:
            return

        # Hide previous tab close button
        tabButton = tabBar.tabButton(self._prevIndex, QTabBar.ButtonPosition.RightSide)
        if tabButton is not None:
            tabButton.resize(0, 0)
            
        # Show current tab close button
        tabButton = tabBar.tabButton(index, QTabBar.ButtonPosition.RightSide)
        if tabButton is not None:
            tabButton.resize(QSize(20, 20))
            tabBar.adjustSize()
            
        self._prevIndex = index
