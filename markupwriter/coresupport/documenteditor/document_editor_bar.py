#!/usr/bin/python

from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
)

class DocumentEditorBar(QWidget):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        
        self.docPathLabel = QLabel("", self)
        
        hLayout = QHBoxLayout(self)
        hLayout.setContentsMargins(0, 11, 0, 11)
        hLayout.setSpacing(0)
        hLayout.addStretch()
        hLayout.addWidget(self.docPathLabel)
        hLayout.addStretch()
        
    def clearDocPathLabel(self):
        self.docPathLabel.clear()
    
    def onNameListReceived(self, nameList: list[str]):
        self.docPathLabel.clear()
        
        text = ""
        count = len(nameList)
        for i in range(count-1):
            text += "{} \u203a ".format(nameList[i])
        
        text += "{}".format(nameList[count-1])
            
        self.docPathLabel.setText(text)
