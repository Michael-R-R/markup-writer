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

import markupwriter.support.doctree.item as dti


class ExportSelectWidget(QDialog):
    def __init__(self, tree: QTreeWidget, parent: QWidget | None) -> None:
        super().__init__(parent)

        self.setWindowTitle("Export (EPUB3)")

        self.dir = ""
        self.value: QTreeWidgetItem = None

        self.gLayout = QGridLayout(self)
        self.gLayout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)

        # Add novel widgets to layout
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

        self.dirLineEdit = QLineEdit("", self)
        self.dirLineEdit.setReadOnly(True)
        self.dirButton = QToolButton(self)
        self.dirButton.setIcon(Icon.MISC_FOLDER)
        self.dirButton.clicked.connect(self._onDirButtonClicked)
        self.gLayout.addWidget(self.dirLineEdit, count + 1, 0)
        self.gLayout.addWidget(
            self.dirButton, count + 1, 1, Qt.AlignmentFlag.AlignRight
        )

    def _onItemSelected(self, item: QTreeWidgetItem):
        if self.dir == "":
            self.reject()
        else:
            self.value = item
            self.accept()

    @pyqtSlot()
    def _onDirButtonClicked(self):
        dir = QFileDialog.getExistingDirectory(
            self,
            "Export Directory",
            "/home",
            QFileDialog.Option.ShowDirsOnly | QFileDialog.Option.DontResolveSymlinks,
        )
        if dir == "":
            self.dir = ""
            self.dirLineEdit.clear()
            return
        
        self.dir = dir
        self.dirLineEdit.setText(dir)
