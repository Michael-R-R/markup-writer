#!/usr/bin/python

from PyQt6.QtCore import (
    Qt,
    pyqtSlot,
)

from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
    QTreeWidget,
    QTreeWidgetItem,
    QDialog,
    QPushButton,
    QLayout,
)

import markupwriter.support.doctree.item as dti


class ExportSelectWidget(QDialog):
    def __init__(self, tree: QTreeWidget, parent: QWidget | None) -> None:
        super().__init__(parent)

        self.setWindowTitle("Export (EPUB3)")

        self.value: QTreeWidgetItem = None
        
        self.gLayout = QGridLayout(self)
        self.gLayout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)

        count = 0
        for i in range(tree.topLevelItemCount()):
            item = tree.topLevelItem(i)
            widget: dti.BaseTreeItem = tree.itemWidget(item, 0)

            if isinstance(widget, dti.NovelFolderItem):
                wtemp = widget.shallowcopy()
                selectButton = QPushButton("Select", self)
                self.gLayout.addWidget(wtemp, count, 0)
                self.gLayout.addWidget(selectButton, count, 1)
                selectButton.clicked.connect(
                    lambda _, val=item: self._onItemSelected(val)
                )
                count += 1

        self.cancelButton = QPushButton("Cancel", self)
        self.cancelButton.clicked.connect(self._onCancelClicked)
        self.gLayout.addWidget(self.cancelButton, count + 1, 0, count + 1, 2)

    def _onItemSelected(self, item: QTreeWidgetItem):
        self.value = item
        self.accept()

    @pyqtSlot()
    def _onCancelClicked(self):
        self.reject()
