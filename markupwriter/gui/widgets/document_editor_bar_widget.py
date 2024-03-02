#!/usr/bin/python

from PyQt6.QtCore import (
    Qt,
    QSize,
)

from PyQt6.QtGui import (
    QAction,
)

from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
    QSpacerItem,
    QSizePolicy,
    QLabel,
    QToolBar,
)

from markupwriter.common.provider import Icon


class DocumentEditorBarWidget(QWidget):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)

        self.stateLabel = QLabel("-- NORMAL --", self)
        self.pathLabel = QLabel("", self)

        self.toolBar = QToolBar(self)
        self.toolBar.setIconSize(QSize(18, 18))
        self.closeAction = QAction(Icon.UNCHECK, "Close", self.toolBar)
        
        wpolicy = QSizePolicy.Policy.Expanding
        hpolicy = QSizePolicy.Policy.Minimum
        lhSpacer = QSpacerItem(0, 0, wpolicy, hpolicy)
        rhSpacer = QSpacerItem(0, 0, wpolicy, hpolicy)

        self.gLayout = QGridLayout(self)
        self.gLayout.addWidget(self.stateLabel, 0, 0, Qt.AlignmentFlag.AlignLeft)
        self.gLayout.addItem(lhSpacer, 0, 1)
        self.gLayout.addWidget(self.pathLabel, 0, 2)
        self.gLayout.addItem(rhSpacer, 0, 3)
        self.gLayout.addWidget(self.toolBar, 0, 4, Qt.AlignmentFlag.AlignRight)

    def reset(self):
        self.pathLabel.clear()
        self.toolBar.clear()
        
    def addPath(self, paths: list[str]):
        text = ""
        count = len(paths)
        for i in range(count - 1):
            text += "{} \u203a ".format(paths[i])

        text += "{}".format(paths[count - 1])

        self.pathLabel.setText(text)
        
    def replaceInPath(self, old: str, new: str):
        text = self.pathLabel.text()
        text = text.replace(old, new)
        self.pathLabel.setText(text)
        
    def addCloseAction(self):
        self.toolBar.addAction(self.closeAction)
