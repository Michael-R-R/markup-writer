#!/usr/bin/python

from PyQt6.QtCore import (
    Qt,
    pyqtSlot,
)

from PyQt6.QtWidgets import (
    QDialog,
    QWidget,
    QGridLayout,
    QTreeWidget,
    QTreeWidgetItem,
    QLineEdit,
    QToolButton,
    QPushButton,
    QLayout,
    QFileDialog,
)

from markupwriter.common.provider import Icon

import markupwriter.support.doctree.item as ti


class ExportDialog(QDialog):
    def __init__(self, tree: QTreeWidget, parent: QWidget | None) -> None:
        super().__init__(parent)

        self.setWindowTitle("Export (EPUB3)")

        self.dir = ""
        self.value: QTreeWidgetItem = None
        self._tree = tree

        self.gLayout = QGridLayout(self)
        self.gLayout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)

        self.dirLineEdit = QLineEdit("", self)
        self.dirLineEdit.setReadOnly(True)
        self.dirLineEdit.setPlaceholderText("Select directory...")

        self.dirButton = QToolButton(self)
        self.dirButton.setIcon(Icon.MISC_FOLDER)
        self.dirButton.clicked.connect(self._onDirButtonClicked)

        self.gLayout.addWidget(self.dirLineEdit, 0, 0)
        self.gLayout.addWidget(self.dirButton, 0, 1, Qt.AlignmentFlag.AlignRight)

    @pyqtSlot()
    def _onDirButtonClicked(self):
        dir = QFileDialog.getExistingDirectory(
            self,
            "Export Directory",
            "/home",
            QFileDialog.Option.ShowDirsOnly | QFileDialog.Option.DontResolveSymlinks,
        )
        if dir == "":
            return

        self.dir = dir
        self.dirLineEdit.setText(dir)
        
        self._buildWidgets()

    def _buildWidgets(self):
        row = 2
        for i in range(self._tree.topLevelItemCount()):
            item = self._tree.topLevelItem(i)
            widget: ti.BaseTreeItem = self._tree.itemWidget(item, 0)

            if isinstance(widget, ti.NovelFolderItem):
                wtemp = widget.shallowcopy()
                selectButton = QPushButton("Select", self)
                self.gLayout.addWidget(wtemp, row, 0)
                self.gLayout.addWidget(selectButton, row, 1)
                selectButton.clicked.connect(
                    lambda _, val=item: self._onItemSelected(val)
                )
                row += 1

    def _onItemSelected(self, item: QTreeWidgetItem):
        if self.dir == "":
            self.reject()
        else:
            self.value = item
            self.accept()
