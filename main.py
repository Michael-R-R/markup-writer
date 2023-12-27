#!/usr/bin/python

import sys

try:
    import PyQt6.QtCore
    import PyQt6.QtWidgets
    import PyQt6.QtGui
except Exception:
    print("ERROR::main::cannot import PyQt6 dependecies")
    sys.exit(1)

from PyQt6.QtCore import (
    QDir,
)

from markupwriter.core import (
    appStart,
    appRun,
    appClose,
)

if __name__ == "__main__":
    appStart()
    status = appRun(sys.argv[1:])
    appClose()

    sys.exit(status)