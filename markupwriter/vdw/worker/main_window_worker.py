#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    pyqtSlot,
)

import markupwriter.vdw.delegate as d


class MainWindowWorker(QObject):
    def __init__(self, mwd: d.MainWindowDelegate, parent: QObject | None) -> None:
        super().__init__(parent)

        self.mwd = mwd
        
    def showStatusBarMsg(self, msg: str, msecs: int):
        sb = self.mwd.view.statusBar()
        sb.showMessage(msg, msecs)
        
    @pyqtSlot(str)
    def onShowPermMsg(self, msg: str):
        sb = self.mwd.view.statusBarWidget
        sb.permLabel.setText(msg)
