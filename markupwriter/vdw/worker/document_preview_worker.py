from PyQt6.QtCore import QObject, pyqtSlot
from PyQt6.QtWidgets import QWidget

import markupwriter.vdw.view as v
import markupwriter.gui.widgets as w


class DocumentPreviewWorker(QObject):
    def __init__(self, dpv: v.DocumentPreviewView, parent: QObject | None) -> None:
        super().__init__(parent)
        
        self.dpv = dpv
        
    @pyqtSlot()
    def onFocusPreviewTriggered(self):
        tw = self.dpv.tabWidget
        tw.setFocus()
        
    @pyqtSlot()
    def onRefreshTriggered(self):
        tw = self.dpv.tabWidget
        index = tw.currentIndex()
        widget: w.PreviewWidget = tw.widget(index)
        if widget is None:
            return
        
        widget.refreshContent()
    
    @pyqtSlot()
    def onToggleTriggered(self):
        tw = self.dpv.tabWidget
        index = tw.currentIndex()
        widget: w.PreviewWidget = tw.widget(index)
        if widget is None:
            return
        
        widget.toggleView()
        
    @pyqtSlot(int)
    def onCloseTabRequested(self, index: int):
        tw = self.dpv.tabWidget
        tw.removeTab(index)
        
    @pyqtSlot(str, str)
    def onFileRemoved(self, title: str, uuid: str):
        index = self._findPageIndex(title, uuid)
        if index < 0:
            return
        tw = self.dpv.tabWidget
        tw.removeTab(index)
    
    @pyqtSlot(str, str, str)
    def onFileRenamed(self, uuid: str, old: str, new: str):
        index = self._findPageIndex(old, uuid)
        if index < 0:
            return
        tw = self.dpv.tabWidget
        widget: w.PreviewWidget = tw.widget(index)
        widget.title = new
        tw.setTabText(index, new)
    
    @pyqtSlot(str, str)
    def onFilePreviewed(self, title: str, uuid: str):
        width = self.dpv.size().width()
        if width <= 0:
            self.dpv.showViewRequested.emit()

        widget = w.PreviewWidget(title, uuid, self.dpv)
        self._addTabPage(title, uuid, widget)
    
    def _addTabPage(self, title: str, uuid: str, widget: QWidget):
        tw = self.dpv.tabWidget
        index = self._findPageIndex(title, uuid)
        if index > -1:
            tw.setCurrentIndex(index)
            return

        tw.addTab(widget, title)
        tw.setCurrentWidget(widget)
        
    def _findPageIndex(self, title: str, uuid: str) -> int:
        tw = self.dpv.tabWidget
        for i in range(tw.count()):
            widget: w.PreviewWidget = tw.widget(i)
            if widget is None:
                continue

            if widget.checkForMatch(title, uuid):
                return i

        return -1
    