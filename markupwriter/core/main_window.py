#!/usr/bin/python

from PyQt6.QtWidgets import (
    QMainWindow,
    QSplitter,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QWidget,
)

from markupwriter.config import (
    config_app
)

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle(config_app.APP_NAME)

        vWidget = QWidget(self)

        hSplitter = QSplitter()
        hSplitter.addWidget(QPushButton("button1", vWidget))
        hSplitter.addWidget(QPushButton("button2", vWidget))
        hSplitter.addWidget(QPushButton("button3", vWidget))

        vLayout = QVBoxLayout(vWidget)
        vLayout.addWidget(QPushButton("Top", vWidget))
        vLayout.addWidget(hSplitter)

        hWidget = QWidget()
        hLayout = QHBoxLayout(hWidget)
        hLayout.addWidget(QPushButton("Bottom1", hWidget))
        hLayout.addWidget(QPushButton("Bottom2", hWidget))
        hLayout.addWidget(QPushButton("Bottom3", hWidget))
        vLayout.addWidget(hWidget)

        vLayout.addStretch()
        
        self.setCentralWidget(vWidget)
        