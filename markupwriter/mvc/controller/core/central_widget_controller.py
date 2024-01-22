#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    QDataStream,
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
        ec.previewRequested.connect(self._onEditorPreviewRequested)
        tc.previewRequested.connect(self._onTreePreviewRequested)

        # --- Editor controller slots --- #
        tc.fileOpened.connect(ec.onFileOpened)
        tc.fileMoved.connect(ec.onFileMoved)
        tc.fileRenamed.connect(ec.onFileRenamed)
        tc.fileRemoved.connect(ec.onFileRemoved)

    @pyqtSlot()
    def onSaveAction(self):
        self.model.docEditorController.onSaveAction()
        
    @pyqtSlot(str, str)
    def _onTreePreviewRequested(self, title: str, uuid: str):
        pc = self.model.docPreviewController
        pc.onPreviewRequested(title, uuid)

    @pyqtSlot(str)
    def _onEditorPreviewRequested(self, uuid: str):
        tc = self.model.docTreeController
        widget = tc.findTreeItem(uuid)
        if widget is None:
            return
        
        pc = self.model.docPreviewController
        pc.onPreviewRequested(widget.title(), uuid)

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
