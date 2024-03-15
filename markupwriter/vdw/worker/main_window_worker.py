#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    pyqtSlot,
)

import markupwriter.vdw.view as v


class MainWindowWorker(QObject):
    def __init__(self, mwv: v.MainWindowView, parent: QObject | None) -> None:
        super().__init__(parent)

        self.mwv = mwv
        
    def showStatusBarMsg(self, msg: str, msecs: int):
        sb = self.mwv.statusBar()
        sb.showMessage(msg, msecs)
        
    @pyqtSlot(str)
    def onShowPermMsg(self, msg: str):
        sb = self.mwv.statusBarWidget
        sb.normLabel.setText(msg)
