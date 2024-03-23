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
    QLabel,
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
        self.setFixedSize(600, 300)

        self.exportDir = ""
        self.value: QTreeWidgetItem = None

        self._tree = tree
        self._isBuilt = False

        self.dirEdit = QLineEdit("", self)
        self.dirEdit.setReadOnly(True)
        self.dirEdit.setPlaceholderText("Select directory...")
        self.dirButton = QToolButton(self)
        self.dirButton.setIcon(Icon.MISC_FOLDER)

        self.coverImgEdit = QLineEdit("")
        self.coverImgEdit.setPlaceholderText("Select cover image...")
        self.coverImgEdit.setReadOnly(True)
        self.coverImgButton = QToolButton()
        self.coverImgButton.setIcon(Icon.MISC_FOLDER)

        self.authorEdit = QLineEdit("")
        self.titleEdit = QLineEdit("")
        self.publisherEdit = QLineEdit("")

        self.gLayout = QGridLayout(self)
        self.gLayout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.gLayout.addWidget(self.dirButton, 0, 0, Qt.AlignmentFlag.AlignLeft)
        self.gLayout.addWidget(self.dirEdit, 0, 1)

        self.dirButton.clicked.connect(self._onDirButtonClicked)
        self.coverImgButton.clicked.connect(self._onImgButtonClicked)

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

        self.exportDir = dir
        self.dirEdit.setText(dir)

        if not self._isBuilt:
            self._buildWidgets()

    @pyqtSlot()
    def _onImgButtonClicked(self):
        path = QFileDialog.getOpenFileName(
            self, "Cover Image", "/home", "Image Files (*.jpg *.png)"
        )
        if path[0] == "":
            return

        self.coverImgEdit.setText(path[0])

    def _buildWidgets(self):
        self.gLayout.addWidget(self.coverImgButton, 1, 0, Qt.AlignmentFlag.AlignLeft)
        self.gLayout.addWidget(self.coverImgEdit, 1, 1)

        self.gLayout.addWidget(QLabel("Author"), 2, 0, Qt.AlignmentFlag.AlignLeft)
        self.gLayout.addWidget(self.authorEdit, 2, 1)

        self.gLayout.addWidget(QLabel("Title"), 3, 0, Qt.AlignmentFlag.AlignLeft)
        self.gLayout.addWidget(self.titleEdit, 3, 1)

        self.gLayout.addWidget(QLabel("Publisher"), 4, 0, Qt.AlignmentFlag.AlignLeft)
        self.gLayout.addWidget(self.publisherEdit, 4, 1)

        row = 5
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
                
        self._isBuilt = True

    def _onItemSelected(self, item: QTreeWidgetItem):
        if self.exportDir == "":
            self.reject()
        else:
            self.value = item
            self.accept()
