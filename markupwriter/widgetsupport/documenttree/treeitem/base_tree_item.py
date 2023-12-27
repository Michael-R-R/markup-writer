#!/usr/bin/python

from PyQt6.QtCore import (
    QDataStream,
)

from PyQt6.QtGui import (
    QIcon,
    QPixmap,
    QColor,
)

from PyQt6.QtWidgets import (
    QWidget,
    QTreeWidgetItem,
    QHBoxLayout,
    QLabel,
)

from markupwriter.config import (
    AppConfig,
)

from markupwriter.support.iconprovider import (
    Icon,
)

class BaseTreeItem(QWidget):
    W_ICON = 1
    W_TITLE = 2
    W_COUNT = 3
    W_ACTIVE = 4
    W_GROUP = 5
    W_PRIORITY = 6

    def __init__(self, title: str, path: str, 
                 item: QTreeWidgetItem, 
                 parent: QWidget):
        super().__init__(parent)

        self._path = path
        self._title = title
        self._wc = "0"
        self._isActive = False
        self._groupCol = QColor(64, 64, 64)
        self._priorityCol = QColor(64, 64, 64)
        self._item = item

        hLayout = QHBoxLayout(self)
        hLayout.setContentsMargins(0, 0, 0, 0)
        hLayout.addWidget(QLabel("icon", self))
        hLayout.addWidget(QLabel("title", self))
        hLayout.addStretch()
        hLayout.addWidget(QLabel("wc", self))
        hLayout.addWidget(QLabel("active", self))
        hLayout.addWidget(QLabel("group", self))
        hLayout.addWidget(QLabel("priority", self))

        self.applyChanges()

    def applyChanges(self):
        self.setTitle(self._title)
        self.setWordCount(self._wc)
        self.setActiveStatus(self._isActive)
        self.setGroupStatus(self._groupCol)
        self.setPriorityStatus(self._priorityCol)

    def path(self) -> str:
        return self._path

    def title(self) -> str:
        return self._title
    
    def wordCount(self) -> str:
        return self._wc

    def isActive(self) -> bool:
        return self._isActive
    
    def groupCol(self) -> QColor:
        return self._groupCol
    
    def priorityCol(self) -> QColor:
        return self._priorityCol
    
    def item(self) -> QTreeWidgetItem:
        return self._item
    
    def setPath(self, path: str):
        if path == "":
            return
        self._path = path

    def setIcon(self, icon: QIcon):
        label: QLabel = self.children()[self.W_ICON]
        label.setPixmap(icon.pixmap(AppConfig.ICON_SIZE))

    def setTitle(self, text: str):
        if text == "":
            return
        self._title = text
        label: QLabel = self.children()[self.W_TITLE]
        label.setText(text)

    def setWordCount(self, text: str):
        if not text.isnumeric():
            return
        self._wc = text
        label: QLabel = self.children()[self.W_COUNT]
        label.setText(text)

    def toggleActiveStatus(self):
        self._isActive = not self._isActive
        label: QLabel = self.children()[self.W_ACTIVE]
        if self._isActive:
            label.setPixmap(Icon.CHECK.pixmap(AppConfig.ICON_SIZE))
        else:
            label.setPixmap(Icon.UNCHECK.pixmap(AppConfig.ICON_SIZE))

    def setActiveStatus(self, status: bool):
        self._isActive = status
        label: QLabel = self.children()[self.W_ACTIVE]
        if status:
            label.setPixmap(Icon.CHECK.pixmap(AppConfig.ICON_SIZE))
        else:
            label.setPixmap(Icon.UNCHECK.pixmap(AppConfig.ICON_SIZE))

    def setGroupStatus(self, color: QColor):
        pix = QPixmap(AppConfig.ICON_SIZE)
        pix.fill(color)
        label: QLabel = self.children()[self.W_GROUP]
        label.setPixmap(pix)

    def setPriorityStatus(self, color: QColor):
        pix = QPixmap(AppConfig.ICON_SIZE)
        pix.fill(color)
        label: QLabel = self.children()[self.W_PRIORITY]
        label.setPixmap(pix)

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        sOut.writeString(self._path)
        sOut.writeString(self._title)
        sOut.writeString(self._wc)
        sOut.writeBool(self._isActive)
        sOut << self._groupCol
        sOut << self._priorityCol
        return sOut
    
    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        self._path = sIn.readString()
        self._title = sIn.readString()
        self._wc = sIn.readString()
        self._isActive = sIn.readBool()
        sIn >> self._groupCol
        sIn >> self._priorityCol
        return sIn
