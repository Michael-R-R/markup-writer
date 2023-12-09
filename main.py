#!/usr/bin/python

import sys

try:
    import PyQt6.QtCore
    import PyQt6.QtWidgets
    import PyQt6.QtGui
except Exception:
    print("ERROR::main::cannot import PyQt6 dependecies")
    sys.exit(1)

from markupwriter.core.application import (
    start,
    run,
    close
)

if __name__ == "__main__":
    start()
    status = run(sys.argv[1:])
    close()

    sys.exit(status)