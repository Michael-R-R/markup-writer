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
    ICON = 1
    TITLE = 2
    WORD_COUNT = 3
    ACTIVE = 4
    GROUP = 5
    PRIORITY = 6

    def __init__(self,
                 path: str,
                 title: str,
                 item: QTreeWidgetItem, 
                 isFolder: bool,
                 parent: QWidget):
        super().__init__(parent)

        self._item = item
        self._path = path
        self._title = title
        self._wordCount = "0"
        self._isActive = False
        self._groupStatus = QColor(64, 64, 64)
        self._priorityStatus = QColor(64, 64, 64)
        self._isFolder = isFolder

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

    isFolder = property(lambda self: self._isFolder, None)

    def applyIcon(self):
        raise NotImplementedError()

    def applyChanges(self):
        self.title = self._title
        self.wordCount = self._wordCount
        self.isActive = self._isActive
        self.groupStatus = self._groupStatus
        self.priorityStatus= self._priorityStatus

    def icon(self, icon: QIcon):
        label: QLabel = self.children()[self.ICON]
        label.setPixmap(icon.pixmap(AppConfig.ICON_SIZE))
    icon = property(None, icon)

    def path(self, text: str):
        if text == "":
            return
        self._path = text
    path = property(lambda self: self._path, path)

    def title(self, text: str):
        if text == "":
            return
        self._title = text
        label: QLabel = self.children()[self.TITLE]
        label.setText(text)
    title = property(lambda x: x._title, title)

    def wordCount(self, text: str):
        if not text.isnumeric():
            return
        self._wordCount = text
        label: QLabel = self.children()[self.WORD_COUNT]
        label.setText(text)
    wordCount = property(lambda self: self._wordCount, wordCount)

    def isActive(self, status: bool):
        self._isActive = status
        label: QLabel = self.children()[self.ACTIVE]
        if status:
            label.setPixmap(Icon.CHECK.pixmap(AppConfig.ICON_SIZE))
        else:
            label.setPixmap(Icon.UNCHECK.pixmap(AppConfig.ICON_SIZE))
    isActive = property(lambda self: self._isActive, isActive)

    def groupStatus(self, color: QColor):
        pix = QPixmap(AppConfig.ICON_SIZE)
        pix.fill(color)
        label: QLabel = self.children()[self.GROUP]
        label.setPixmap(pix)
    groupStatus = property(lambda self: self._groupStatus, groupStatus)

    def priorityStatus(self, color: QColor):
        pix = QPixmap(AppConfig.ICON_SIZE)
        pix.fill(color)
        label: QLabel = self.children()[self.PRIORITY]
        label.setPixmap(pix)
    priorityStatus = property(lambda self: self._priorityStatus, priorityStatus)

    def toggleActive(self):
        self.isActive = not self.isActive

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        sOut.writeString(self._path)
        sOut.writeString(self._title)
        sOut.writeString(self._wordCount)
        sOut.writeBool(self._isActive)
        sOut << self._groupStatus
        sOut << self._priorityStatus
        sOut.writeBool(self._isFolder)
        return sOut
    
    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        self._path = sIn.readString()
        self._title = sIn.readString()
        self._wordCount = sIn.readString()
        self._isActive = sIn.readBool()
        sIn >> self._groupStatus
        sIn >> self._priorityStatus
        self._isFolder = sIn.readBool()
        return sIn