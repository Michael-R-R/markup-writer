#!/usr/bin/python

from PyQt6.QtCore import (
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
from markupwriter.common.provider import Icon


class MainWindowView(QMainWindow):
    closing = pyqtSignal()
    
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)
        
        self.setWindowIcon(Icon.BOOKS) # TODO get better app icon
        
        self.resize(AppConfig.mainWindowSize)
        
    def updateWindowTitle(self):
        self.setWindowTitle(AppConfig.fullWindowTitle())
        
    def showStatusMsg(self, text: str, msecs: int = 1000):
        self.statusBar().showMessage(text, msecs)
        
    def resizeEvent(self, e: QResizeEvent | None) -> None:
        AppConfig.mainWindowSize = e.size()
        return super().resizeEvent(e)
    
    def closeEvent(self, e: QCloseEvent | None) -> None:
        self.closing.emit()
        super().closeEvent(e)
