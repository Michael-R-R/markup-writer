#!/usr/bin/python

from PyQt6.QtCore import (
    Qt,
    QDataStream,
    pyqtSignal,
    pyqtSlot,
    QSize,
)

from PyQt6.QtGui import (
    QKeyEvent,
)

from PyQt6.QtWidgets import (
    QWidget,
    QTabWidget,
    QTabBar,
    QToolButton,
)

from markupwriter.common.provider import Icon

import markupwriter.gui.widgets as w


class PreviewTabWidget(QTabWidget):
    countChanged = pyqtSignal(int)
    
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)

        self._prevIndex = -1

        self.setTabsClosable(True)
        self.setMovable(True)
        self.setContentsMargins(0, 0, 0, 0)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.currentChanged.connect(self._onCurrentChanged)
        
    def addTab(self, widget: w.PreviewWidget, title: str) -> None:
        super().addTab(widget, title)
        
        self.countChanged.emit(self.count())
        
    def tabInserted(self, index: int) -> None:
        super().tabInserted(index)
        
        tabBar = self.tabBar()
        closeButton = QToolButton(tabBar)
        closeButton.setIcon(Icon.UNCHECK)
        closeButton.clicked.connect(self._onCloseButtonClicked)
        tabBar.setTabButton(index, QTabBar.ButtonPosition.RightSide, closeButton)
        
        self.countChanged.emit(self.count())
        
    def tabRemoved(self, index: int) -> None:
        super().tabRemoved(index)
        
        self.countChanged.emit(self.count())
    
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
        
    def scrollContentX(self, direction: int):
        i = self.currentIndex()
        widget: w.PreviewWidget = self.widget(i)
        if widget is None:
            return
        widget.scrollContentX(direction)
        
    def scrollContentY(self, direction: int):
        i = self.currentIndex()
        widget: w.PreviewWidget = self.widget(i)
        if widget is None:
            return
        widget.scrollContentY(direction)
        
    def keyPressEvent(self, e: QKeyEvent | None) -> None:
        match e.key():
            case Qt.Key.Key_A:
                self.navigateTabs(-1)
            case Qt.Key.Key_D:
                self.navigateTabs(1)
            case Qt.Key.Key_H:
                self.scrollContentX(-1)
            case Qt.Key.Key_J:
                self.scrollContentY(1)
            case Qt.Key.Key_K:
                self.scrollContentY(-1)
            case Qt.Key.Key_L:
                self.scrollContentX(1)
            case _: return super().keyPressEvent(e)
            
    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        count = self.count()
        sout.writeInt(count)
        
        for i in range(count):
            widget: w.PreviewWidget = self.widget(i)
            sout.writeQString(widget.title)
            sout.writeQString(widget.uuid)
        
        return sout
    
    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        count = sin.readInt()
        
        for _ in range(count):
            title = sin.readQString()
            uuid = sin.readQString()
            widget = w.PreviewWidget(title, uuid, self)
            self.addTab(widget, title)
        
        return sin
