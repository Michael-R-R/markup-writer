#!/usr/bin/python

from PyQt6.QtCore import (
    Qt,
)

from PyQt6.QtGui import (
    QTextCursor,
)


class KeyProcessor(object):
    def process(cursor: QTextCursor, key: int) -> QTextCursor:
        match key:
            case Qt.Key.Key_BracketLeft: return KeyProcessor._handleLeftBracket(cursor)
            case _: return cursor
    
    def _handleLeftBracket(cursor: QTextCursor) -> QTextCursor:
        cursor.insertText("]")
        cursor.movePosition(QTextCursor.MoveOperation.Left)
        return cursor
