#!/usr/bin/python

from PyQt6.QtCore import (
    pyqtSlot,
)

from PyQt6.QtWidgets import (
    QDialog,
    QWidget,
    QLayout,
    QHBoxLayout,
    QVBoxLayout,
    QGroupBox,
    QRadioButton,
    QLineEdit,
    QPushButton,
    QToolButton,
    QFileDialog,
    QSizePolicy,
)

from markupwriter.common.provider import Icon

import markupwriter.support.doctree.item as ti


class ImportDialog(QDialog):
    def __init__(self, filter: str, parent: QWidget | None) -> None:
        super().__init__(parent)
        
        self.setWindowTitle("Create Item")
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)
        
        self.path: str = None
        self.value: ti.BaseFileItem = None
        self._filter = filter
        self._isBuilt = False
        
        self._pathLineEdit = QLineEdit("", self)
        self._pathLineEdit.setReadOnly(True)
        self._pathLineEdit.setPlaceholderText("Select file...")
        
        self._dirButton = QToolButton(self)
        self._dirButton.setIcon(Icon.MISC_FOLDER)
        self._dirButton.clicked.connect(self._onDirButtonClicked)
        
        self._titleButton = QRadioButton("Title")
        self._chapterButton = QRadioButton("Chapter")
        self._sceneButton = QRadioButton("Scene")
        self._sectionButton = QRadioButton("Section")
        self._miscButton = QRadioButton("Misc")
        self._rbGroupBox = QGroupBox()
        self._nameLineEdit = QLineEdit("Default")
        self._cancelButton = QPushButton("Cancel")
        self._okButton = QPushButton("Ok")
        
        hLayout = QHBoxLayout()
        hLayout.addWidget(self._pathLineEdit)
        hLayout.addWidget(self._dirButton)
        
        self._vLayout = QVBoxLayout(self)
        self._vLayout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self._vLayout.addLayout(hLayout)
        
        self._cancelButton.clicked.connect(self.onCancelClicked)
        self._okButton.clicked.connect(self.onOkClicked)
        
    @pyqtSlot()
    def _onDirButtonClicked(self):
        path = QFileDialog.getOpenFileName(
            self,
            "Import File",
            "/home",
            self._filter
        )
        
        if path[0] == "":
            return
        
        self.path = path[0]
        self._pathLineEdit.setText(path[0])
        
        self._build()
        
    def _build(self):
        if self._isBuilt:
            return
        
        rbLayout = QHBoxLayout()
        rbLayout.addWidget(self._titleButton)
        rbLayout.addWidget(self._chapterButton)
        rbLayout.addWidget(self._sceneButton)
        rbLayout.addWidget(self._sectionButton)
        rbLayout.addWidget(self._miscButton)
        
        self._rbGroupBox.setLayout(rbLayout)
        self._miscButton.setChecked(True)
        
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self._cancelButton)
        buttonLayout.addWidget(self._okButton)
        
        self._vLayout.addWidget(self._rbGroupBox)
        self._vLayout.addWidget(self._nameLineEdit)
        self._vLayout.addLayout(buttonLayout)
        
        self._isBuilt = True

    @pyqtSlot()
    def onCancelClicked(self):
        self.reject()
        
    @pyqtSlot()
    def onOkClicked(self):
        name = self._nameLineEdit.text()
        if name == "":
            self.reject()
            return
        
        if self._titleButton.isChecked():
            self.value = ti.TitleFileItem(name)
        elif self._chapterButton.isChecked():
            self.value = ti.ChapterFileItem(name)
        elif self._sceneButton.isChecked():
            self.value = ti.SceneFileItem(name)
        elif self._sectionButton.isChecked():
            self.value = ti.SectionFileItem(name)
        elif self._miscButton.isChecked():
            self.value = ti.MiscFileItem(name)
        
        self.accept()