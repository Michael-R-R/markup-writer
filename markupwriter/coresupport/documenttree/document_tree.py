#!/usr/bin/python

from PyQt6.QtCore import (
    Qt,
    QDataStream,
    pyqtSignal,
)

from PyQt6.QtGui import (
    QDragEnterEvent,
    QDropEvent,
    QMouseEvent,
)

from PyQt6.QtWidgets import (
    QTreeWidget,
    QTreeWidgetItem,
    QWidget,
    QFrame,
)

from .treeitem import (
    ITEM_FLAG,
    BaseTreeItem,
    NovelFolderItem,
    PlotFolderItem,
    TimelineFolderItem,
    CharsFolderItem,
    LocFolderItem,
    ObjFolderItem,
    TrashFolderItem,
    MiscFolderItem,
)

import markupwriter.coresupport.documenttree as dt

class DocumentTree(QTreeWidget):
    fileAdded = pyqtSignal(str)
    fileRemoved = pyqtSignal(str)
    fileDoubleClicked = pyqtSignal(str)

    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.helper = dt.DocumentTreeHelper(self)
        self.draggedItem = None

        self.addItemWidget(PlotFolderItem("Plot", QTreeWidgetItem(), self), False)
        self.addItemWidget(TimelineFolderItem("Timeline", QTreeWidgetItem(), self), False)
        self.addItemWidget(CharsFolderItem("Characters", QTreeWidgetItem(), self), False)
        self.addItemWidget(LocFolderItem("Locations", QTreeWidgetItem(), self), False)
        self.addItemWidget(ObjFolderItem("Objects", QTreeWidgetItem(), self), False)
        self.addItemWidget(TrashFolderItem("Trash", QTreeWidgetItem(), self), False)

        self.setDragEnabled(True)
        self.setExpandsOnDoubleClick(False)
        self.setUniformRowHeights(True)
        self.setAllColumnsShowFocus(True)
        self.setDragDropMode(self.DragDropMode.InternalMove)
        self.setSelectionMode(self.SelectionMode.SingleSelection)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setHeaderHidden(True)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.itemDoubleClicked.connect(self.helper.onItemDoubleClick)
        self.customContextMenuRequested.connect(self.helper.onContextMenuRequest)

    def addItemWidget(self, item: BaseTreeItem, isActive: bool = True):
        parent = self.currentItem()
        if parent is None:
            self.addTopLevelItem(item.item)
        elif not item.hasFlag(ITEM_FLAG.draggable):
            self.addTopLevelItem(item.item)
        else:
            parent.addChild(item.item)
                
        self.setItemWidget(item.item, 0, item)
        if isActive:
            self.setCurrentItem(item.item)

        if item.hasFlag(ITEM_FLAG.file):
            self.fileAdded.emit(item.UUID())

    def removeItem(self, item: QTreeWidgetItem, parent: QTreeWidgetItem | None):
        for i in range(item.childCount()-1, -1, -1):
            child = item.child(i)
            self.removeItem(child, item)
        
        widget: BaseTreeItem = self.itemWidget(item, 0)
        if widget.hasFlag(ITEM_FLAG.file):
            self.fileRemoved.emit(widget.UUID())

        if parent is None:
            index = self.indexOfTopLevelItem(item)
            self.takeTopLevelItem(index)
        else:
            parent.removeChild(item)
        
        self.removeItemWidget(item, 0)
        self.clearSelection()
        self.setCurrentItem(None)

    def translateItem(self, direction: int):
        item = self.currentItem()
        if item is None:
            return
        
        parent = item.parent()
        if parent is None: # root index
            size = self.topLevelItemCount()
            index = self.indexFromItem(item, 0).row()
            self.insertItemAt(item, parent, (index + direction) % size)
        else: # child index
            size = parent.childCount()
            index = parent.indexOfChild(item)
            self.insertItemAt(item, parent, (index + direction) % size)

    def moveItemTo(self,
                   item: QTreeWidgetItem,
                   target: QTreeWidgetItem | None):
        widgetList = self.takeItemOut(item)
        if target is None: # add to root
            self.addTopLevelItem(item)
        else: # add to target
            target.addChild(item)

        self.setItemWidgetList(widgetList)
        self.setCurrentItem(item)

    def insertItemAt(self,
                     item: QTreeWidgetItem,
                     target: QTreeWidgetItem | None,
                     targetIndex: int):
        widgetList = self.takeItemOut(item)
        if target is None: # insert to root
            self.insertTopLevelItem(targetIndex, item)
        else: # insert to target
            target.insertChild(targetIndex, item)

        self.setItemWidgetList(widgetList)
        self.setCurrentItem(item)

    def takeItemOut(self, item: QTreeWidgetItem) -> list[BaseTreeItem]:
        widgetList = self.copyWidgets(item, list())
        parent = item.parent()
        if parent is None: # is root item
            index = self.indexFromItem(item, 0).row()
            item = self.takeTopLevelItem(index)
        else: # is child item
            index = parent.indexOfChild(item)
            item = parent.takeChild(index)

        return widgetList
    
    def copyWidgets(self,
                    parent: QTreeWidgetItem,
                    itemList: list[BaseTreeItem]) -> list[BaseTreeItem]:
        result = itemList

        for i in range(parent.childCount()):
            child = parent.child(i)
            result = self.copyWidgets(child, result)

        widget: BaseTreeItem = self.itemWidget(parent, 0)
        result.append(widget.shallowcopy())

        return result
    
    def setItemWidgetList(self, items: list[BaseTreeItem]):
        for i in items:
            self.setItemWidget(i.item, 0, i)

    def isItemInTrash(self, item: QTreeWidgetItem) -> bool:
        trash = self.findTrashFolder()

        prev = None
        curr = item.parent()
        while curr is not None:
            prev = curr
            curr = curr.parent()

        return prev == trash

    def findTrashFolder(self) -> QTreeWidgetItem | None:
        for i in range(self.topLevelItemCount()-1, -1, -1):
            item = self.topLevelItem(i)
            widget = self.itemWidget(item, 0)
            if isinstance(widget, TrashFolderItem):
                return item
        return None

    def dragEnterEvent(self, e: QDragEnterEvent) -> None:
        self.helper.onDragEnterEvent(super(), e)
    
    def dropEvent(self, e: QDropEvent) -> None:
        self.helper.onDropEvent(super(), e)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        self.helper.onMousePressEvent(super(), e)

    def _writeHelper(self,
                     sOut: QDataStream,
                     iParent: QTreeWidgetItem):
        cCount = iParent.childCount()
        sOut.writeInt(cCount)

        for i in range(cCount):
            iChild = iParent.child(i)
            self._writeHelper(sOut, iChild)
            wChild: BaseTreeItem = self.itemWidget(iChild, 0)
            sOut.writeQString(wChild.__class__.__name__)
            sOut << wChild

    def _readHelper(self,
                    sIn: QDataStream,
                    iParent: QTreeWidgetItem):
        cCount = sIn.readInt()

        for i in range(cCount):
            iChild = QTreeWidgetItem()
            self._readHelper(sIn, iChild)
            type = sIn.readQString()
            wChild = self._factoryCreate(type)
            sIn >> wChild
            wChild.item = iChild
            
            iParent.addChild(iChild)
            self.setItemWidget(iChild, 0, wChild)

    def _factoryCreate(self, type: str) -> BaseTreeItem | None:
        match type:
            case NovelFolderItem.__name__:
                return NovelFolderItem()
            case CharsFolderItem.__name__:
                return CharsFolderItem()
            case LocFolderItem.__name__:
                return LocFolderItem()
            case MiscFolderItem.__name__:
                return MiscFolderItem()
            case ObjFolderItem.__name__:
                return ObjFolderItem()
            case PlotFolderItem.__name__:
                return PlotFolderItem()
            case TimelineFolderItem.__name__:
                return TimelineFolderItem()
            case TrashFolderItem.__name__:
                return TrashFolderItem()
            case _:
                return None

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        iCount = self.topLevelItemCount()
        sOut.writeInt(iCount)

        # Top level items
        for i in range(iCount):
            iParent = self.topLevelItem(i)
            wParent: BaseTreeItem = self.itemWidget(iParent, 0)
            sOut.writeQString(wParent.__class__.__name__)
            sOut << wParent

            # Child level items
            self._writeHelper(sOut, iParent)

        return sOut
    
    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        self.clear()

        iCount = sIn.readInt()

        # Top level items
        for i in range(iCount):
            iParent = QTreeWidgetItem()
            type = sIn.readQString()
            wParent = self._factoryCreate(type)
            sIn >> wParent
            wParent.item = iParent

            # Child level items
            self._readHelper(sIn, iParent)

            self.addTopLevelItem(iParent)
            self.setItemWidget(iParent, 0, wParent)

        return sIn
    