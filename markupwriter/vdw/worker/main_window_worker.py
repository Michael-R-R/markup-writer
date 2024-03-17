#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    pyqtSlot,
)

from PyQt6.QtWidgets import (
    QWidget,
    QMenuBar,
)

import markupwriter.vdw.view as v


class MainWindowWorker(QObject):
    def __init__(self, mwv: v.MainWindowView, parent: QObject | None) -> None:
        super().__init__(parent)

        self.mwv = mwv
        
    def setMenuBar(self, menubar: QMenuBar):
        self.mwv.setMenuBar(menubar)
        
    def setCentralWidget(self, widget: QWidget):
        self.mwv.setCentralWidget(widget)
        
    def setWindowTitle(self, title: str | None):
        self.mwv.setWindowTitle(title)
        
    def showStatusBarMsg(self, msg: str, msecs: int):
        sb = self.mwv.statusBar()
        sb.showMessage(msg, msecs)
        
    def startAutoSaveDocTimer(self):
        self.mwv.autoSaveDocTimer.start()
        
    def startAutoSaveProjTimer(self):
        self.mwv.autoSaveProTimer.start()
        
    @pyqtSlot(str)
    def onShowPermMsg(self, msg: str):
        sb = self.mwv.statusBarWidget
        sb.normLabel.setText(msg)
