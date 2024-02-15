#!/usr/bin/python

from PyQt6.QtCore import (
    QDataStream,
    pyqtSignal,
)

from PyQt6.QtGui import (
    QCloseEvent, 
    QResizeEvent,
)

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
)

from markupwriter.config import AppConfig
from markupwriter.common.provider import Icon, Style

import markupwriter.gui.widgets as w


class MainWindowView(QMainWindow):
    closing = pyqtSignal()
    
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)
        
        self.statusBarWidget = w.StatusBarWidget(self)
        
        self.setWindowIcon(Icon.BOOKS) # TODO get better app icon
        self.setWindowTitle(AppConfig.APP_NAME)
        self.setStatusBar(self.statusBarWidget)
        self.setStyleSheet(Style.MAIN_WINDOW)
        self.resize(AppConfig.mainWindowSize)
        
    def resizeEvent(self, e: QResizeEvent | None) -> None:
        AppConfig.mainWindowSize = e.size()
        
        return super().resizeEvent(e)
        
    def closeEvent(self, e: QCloseEvent | None) -> None:
        self.closing.emit()
        return super().closeEvent(e)
        
    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        return sout
    
    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        return sin