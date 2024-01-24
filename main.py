#!/usr/bin/python

import os
import sys

try:
    import PyQt6.QtCore
    import PyQt6.QtWidgets
    import PyQt6.QtGui
except Exception:
    print("ERROR::main::cannot import PyQt6 dependecies")
    sys.exit(1)

from markupwriter.application import (
    Application,
)

if __name__ == "__main__":
    workingDir = os.path.dirname(__file__)
    
    Application.start(workingDir)
    Application.run(sys.argv[1:])
    Application.close()

    sys.exit(Application.status)