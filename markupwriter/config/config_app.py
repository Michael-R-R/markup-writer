#!/usr/bin/python

from PyQt6.QtCore import (
    QDataStream,
)

class Config:
    APP_NAME = "Markup Writer"

    def __rlshift__(self, sOut: QDataStream) -> QDataStream:
        return sOut
    
    def __rrshift__(self, sIn: QDataStream) -> QDataStream:
        return sIn