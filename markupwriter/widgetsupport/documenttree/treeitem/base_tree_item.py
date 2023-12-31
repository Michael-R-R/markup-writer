#!/usr/bin/python

from PyQt6.QtCore import (
    QDataStream,
    QPoint,
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
                 title: str,
                 isDraggable: bool,
                 isEditable: bool,
                 isFolder: bool,
                 item: QTreeWidgetItem, 
                 parent: QWidget):
        super().__init__(parent)

        self._item = item
        self._title = title
        self._wordCount = "0"
        self._isActive = False
        self._groupStatus = QColor(64, 64, 64)
        self._priorityStatus = QColor(64, 64, 64)
        self._isDraggable = isDraggable
        self._isEditable = isEditable
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

    def shallowcopy(self):
        raise NotImplementedError()

    def applyIcon(self):
        raise NotImplementedError()

    def applyChanges(self):
        self.applyIcon()
        self.title = self._title
        self.wordCount = self._wordCount
        self.isActive = self._isActive
        self.groupStatus = self._groupStatus
        self.priorityStatus= self._priorityStatus

    def isFolder(self) -> bool:
        return self._isFolder
    
    def isDraggable(self) -> bool:
        return self._isDraggable
    isDraggable = property(lambda self: self._isDraggable, isDraggable)

    def isEditable(self) -> bool:
        return self._isEditable
    isEditable = property(lambda self: self._isEditable, isEditable)

    def item(self, val: QTreeWidgetItem):
        self._item = val
    item = property(lambda self: self._item, item)

    def icon(self, icon: QIcon):
        label: QLabel = self.children()[self.ICON]
        label.setPixmap(icon.pixmap(AppConfig.ICON_SIZE))
    icon = property(None, icon)

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
        sOut.writeQString(self._title)
        sOut.writeQString(self._wordCount)
        sOut.writeBool(self._isActive)
        sOut << self._groupStatus
        sOut << self._priorityStatus
        sOut.writeBool(self._isDraggable)
        sOut.writeBool(self._isEditable)
        sOut.writeBool(self._isFolder)
        return sOut
    
    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        self._title = sIn.readQString()
        self._wordCount = sIn.readQString()
        self._isActive = sIn.readBool()
        sIn >> self._groupStatus
        sIn >> self._priorityStatus
        self._isDraggable = sIn.readBool()
        self._isEditable = sIn.readBool()
        self._isFolder = sIn.readBool()
        return sIn
