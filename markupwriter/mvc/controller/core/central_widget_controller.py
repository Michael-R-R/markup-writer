#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    QDataStream,
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
