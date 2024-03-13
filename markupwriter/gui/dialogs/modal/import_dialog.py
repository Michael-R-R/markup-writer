#!/usr/bin/python

from PyQt6.QtCore import (
    Qt,
    pyqtSlot,
)

from PyQt6.QtWidgets import (
    QDialog,
    QWidget,
    QLayout,
    QHBoxLayout,
    QGridLayout,
    QGroupBox,
    QRadioButton,
    QLineEdit,
    QPushButton,
    QToolButton,
    QFileDialog,
)

from markupwriter.common.provider import Icon

import markupwriter.support.doctree.item as ti


class ImportDialog(QDialog):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)
        
        self.setWindowTitle("Create Item")
        
        self.path: str = None
        self.value: ti.BaseFileItem = None
        
        self.pathLineEdit = QLineEdit("", self)
        self.pathLineEdit.setReadOnly(True)
        self.pathLineEdit.setPlaceholderText("Select file...")
        
        self.dirButton = QToolButton(self)
        self.dirButton.setIcon(Icon.MISC_FOLDER)
        self.dirButton.clicked.connect(self._onDirButtonClicked)
        
        self.gLayout = QGridLayout(self)
        self.gLayout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.gLayout.addWidget(self.pathLineEdit, 0, 0)
        self.gLayout.addWidget(self.dirButton, 0, 1, Qt.AlignmentFlag.AlignRight)
        
    @pyqtSlot()
    def _onDirButtonClicked(self):
        path = QFileDialog.getOpenFileName(
            self,
            "Import File",
            "/home"
        )
        
        if path[0] == "":
            return
        
        self.path = path[0]
        self.pathLineEdit.setText(path[0])
        
        self._build()
        
    def _build(self):
        self.titleButton = QRadioButton("Title", self)
        self.chapterButton = QRadioButton("Chapter", self)
        self.sceneButton = QRadioButton("Scene", self)
        self.sectionButton = QRadioButton("Section", self)
        self.miscButton = QRadioButton("Misc", self)
        self.miscButton.setChecked(True)
        
        self.hLayout = QHBoxLayout()
        self.hLayout.addWidget(self.titleButton)
        self.hLayout.addWidget(self.chapterButton)
        self.hLayout.addWidget(self.sceneButton)
        self.hLayout.addWidget(self.sectionButton)
        self.hLayout.addWidget(self.miscButton)
        
        self.groupBox = QGroupBox(self)
        self.groupBox.setLayout(self.hLayout)
        
        self.nameLineEdit = QLineEdit("Default", self)
        
        self.cancelButton = QPushButton("Cancel", self)
        self.okButton = QPushButton("Ok", self)
        
        self.gLayout.addWidget(self.groupBox, 1, 0, 2, 2)
        self.gLayout.addWidget(self.nameLineEdit, 3, 0, 4, 2)
        self.gLayout.addWidget(self.cancelButton, 5, 0)
        self.gLayout.addWidget(self.okButton, 5, 1)
        
        self.cancelButton.clicked.connect(self.onCancelClicked)
        self.okButton.clicked.connect(self.onOkClicked)

    @pyqtSlot()
    def onCancelClicked(self):
        self.reject()
        
    @pyqtSlot()
    def onOkClicked(self):
        name = self.nameLineEdit.text()
        if name == "":
            self.reject()
            return
        
        if self.titleButton.isChecked():
            self.value = ti.TitleFileItem(name)
        elif self.chapterButton.isChecked():
            self.value = ti.ChapterFileItem(name)
        elif self.sceneButton.isChecked():
            self.value = ti.SceneFileItem(name)
        elif self.sectionButton.isChecked():
            self.value = ti.SectionFileItem(name)
        elif self.miscButton.isChecked():
            self.value = ti.MiscFileItem(name)
        
        self.accept()