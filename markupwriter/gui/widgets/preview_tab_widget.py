#!/usr/bin/python

from PyQt6.QtCore import (
    Qt,
    pyqtSlot,
    QSize,
)
from PyQt6.QtGui import QKeyEvent

from PyQt6.QtWidgets import (
    QWidget,
    QTabWidget,
    QTabBar,
    QToolButton,
)

from markupwriter.common.provider import Icon


class PreviewTabWidget(QTabWidget):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)

        self._prevIndex = -1

        self.setTabsClosable(True)
        self.setMovable(True)
        self.setContentsMargins(0, 0, 0, 0)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.currentChanged.connect(self._onCurrentChanged)
        
    def tabInserted(self, index: int) -> None:
        super().tabInserted(index)
        
        tabBar = self.tabBar()
        closeButton = QToolButton(tabBar)
        closeButton.setIcon(Icon.UNCHECK)
        closeButton.clicked.connect(self._onCloseButtonClicked)
        tabBar.setTabButton(index, QTabBar.ButtonPosition.RightSide, closeButton)
    
    @pyqtSlot(int)
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
        
    @pyqtSlot()
    def _onCloseButtonClicked(self):
        index = self.currentIndex()
        self.tabCloseRequested.emit(index)
        
    def navigateTabs(self, direction: int):
        count = self.count()
        if count < 1:
            return
        
        index = self.currentIndex()
        index = (index + direction) % count
        
        self.setCurrentIndex(index)
        
    def keyPressEvent(self, e: QKeyEvent | None) -> None:
        match e.key():
            case Qt.Key.Key_A:
                self.navigateTabs(-1)
            case Qt.Key.Key_D:
                self.navigateTabs(1)
            case _: return super().keyPressEvent(e)
