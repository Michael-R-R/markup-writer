from PyQt6.QtCore import QObject, pyqtSlot
from PyQt6.QtWidgets import QWidget

import markupwriter.vdw.delegate as d
import markupwriter.gui.widgets as w


class DocumentPreviewWorker(QObject):
    def __init__(self, dpd: d.DocumentPreviewDelegate, parent: QObject | None) -> None:
        super().__init__(parent)
        
        self.dpd = dpd
        
    @pyqtSlot()
    def onFocusPreviewTriggered(self):
        tw = self.dpd.view.tabWidget
        tw.setFocus()
        
    @pyqtSlot(int)
    def onCloseTabRequested(self, index: int):
        tw = self.dpd.view.tabWidget
        tw.removeTab(index)
        
    @pyqtSlot(str, str)
    def onFileRemoved(self, title: str, uuid: str):
        index = self._findPageIndex(title, uuid)
        if index < 0:
            return
        tw = self.dpd.view.tabWidget
        tw.removeTab(index)
    
    @pyqtSlot(str, str, str)
    def onFileRenamed(self, uuid: str, old: str, new: str):
        index = self._findPageIndex(old, uuid)
        if index < 0:
            return
        tw = self.dpd.view.tabWidget
        widget: w.DocumentPreviewWidget = tw.widget(index)
        widget.title = new
        tw.setTabText(index, new)
    
    @pyqtSlot(str, str)
    def onFilePreviewed(self, title: str, uuid: str):
        width = self.dpd.view.size().width()
        if width <= 0:
            self.dpd.showViewRequested.emit()

        widget = w.DocumentPreviewWidget(title, uuid, self.dpd.view)
        self._addTabPage(title, uuid, widget)
    
    def _addTabPage(self, title: str, uuid: str, widget: QWidget):
        tw = self.dpd.view.tabWidget
        index = self._findPageIndex(title, uuid)
        if index > -1:
            tw.setCurrentIndex(index)
            return

        tw.addTab(widget, title)
        tw.setCurrentWidget(widget)
        
    def _findPageIndex(self, title: str, uuid: str) -> int:
        tw = self.dpd.view.tabWidget
        for i in range(tw.count()):
            widget: w.DocumentPreviewWidget = tw.widget(i)
            if widget is None:
                continue

            if widget.checkForMatch(title, uuid):
                return i

        return -1
    