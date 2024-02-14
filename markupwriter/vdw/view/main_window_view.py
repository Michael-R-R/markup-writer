#!/usr/bin/python

from PyQt6.QtCore import (
    QDataStream,
    pyqtSignal,
    QSize,
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
from markupwriter.common.provider import Icon


class MainWindowView(QMainWindow):
    closing = pyqtSignal()
    resized = pyqtSignal(QSize)
    
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)
        
        self.setWindowIcon(Icon.BOOKS) # TODO get better app icon
        self.setWindowTitle(AppConfig.APP_NAME)
        self.resize(AppConfig.mainWindowSize)
        
    def resizeEvent(self, e: QResizeEvent | None) -> None:
        self.resized.emit(e.size())
        return super().resizeEvent(e)
        
    def closeEvent(self, e: QCloseEvent | None) -> None:
        self.closing.emit()
        return super().closeEvent(e)
        
    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        return sout
    
    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        return sin