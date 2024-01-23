#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    QDataStream,
    pyqtSignal,
    pyqtSlot,
)

from markupwriter.mvc.model.core import (
    CentralWidget,
)

from markupwriter.mvc.view.core import (
    CentralWidgetView,
)

from markupwriter.config import AppConfig


class CentralWidgetController(QObject):
    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)

        self.model = CentralWidget(self)
        self.view = CentralWidgetView(None)

    def setup(self):
        self.model.docTreeController.setup()
        self.model.docEditorController.setup()
        self.model.docPreviewController.setup()

        self.view.lhSplitter.insertWidget(0, self.model.docTreeController.view)
        self.view.rhSplitter.insertWidget(0, self.model.docEditorController.view)
        self.view.rhSplitter.addWidget(self.model.docPreviewController.view)
        self.view.rvSplitter.addWidget(self.model.consoleController.view)

        self.view.lhSplitter.setSizes(
            [
                AppConfig.docTreeSize.width(),
                AppConfig.docEditorSize.width() + AppConfig.docPreviewSize.width(),
            ]
        )

        self.view.rhSplitter.setSizes(
            [
                AppConfig.docEditorSize.width(),
                AppConfig.docPreviewSize.width(),
            ]
        )

        self.view.rvSplitter.setSizes(
            [
                AppConfig.docEditorSize.height(),
                AppConfig.consoleSize.height(),
            ]
        )

        # Controllers
        ec = self.model.docEditorController
        tc = self.model.docTreeController

        # --- Central controller slots --- #
        ec.filePreviewed.connect(self._onEditorFilePreviewed)
        tc.filePreviewed.connect(self._onTreeFilePreviewed)
        tc.fileRemoved.connect(self._onFileRemoved)
        tc.fileOpened.connect(self._onFileOpened)
        tc.fileMoved.connect(self._onFileMoved)
        tc.fileRenamed.connect(self._onFileRenamed)
        
    @pyqtSlot(str, str)
    def _onTreeFilePreviewed(self, title: str, uuid: str):
        pc = self.model.docPreviewController
        pc.onFilePreviewed(title, uuid)

    @pyqtSlot(str)
    def _onEditorFilePreviewed(self, uuid: str):
        tc = self.model.docTreeController
        widget = tc.findTreeItem(uuid)
        if widget is None:
            return
        
        pc = self.model.docPreviewController
        pc.onFilePreviewed(widget.title(), uuid)
        
    @pyqtSlot(str)
    def _onFileRemoved(self, uuid: str):
        self.model.docEditorController.onFileRemoved(uuid)
        
    @pyqtSlot(str, list)
    def _onFileOpened(self, uuid: str, pathList: list[str]):
        self.model.docEditorController.onFileOpened(uuid, pathList)
        
    @pyqtSlot(str, list)
    def _onFileMoved(self, uuid: str, pathList: list[str]):
        self.model.docEditorController.onFileMoved(uuid, pathList)
        
    @pyqtSlot(str, str, str)
    def _onFileRenamed(self, uuid: str, old: str, new: str):
        self.model.docEditorController.onFileRenamed(uuid, old, new)

    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        sout << self.model.docTreeController
        sout << self.model.docEditorController
        sout << self.model.docPreviewController
        sout << self.model.consoleController
        return sout

    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        sin >> self.model.docTreeController
        sin >> self.model.docEditorController
        sin >> self.model.docPreviewController
        sin >> self.model.consoleController
        return sin
