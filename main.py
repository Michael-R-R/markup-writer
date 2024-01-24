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
    wd = os.path.dirname(__file__)
    
    Application.start(wd)
    Application.run(sys.argv[1:])
    Application.close()

    sys.exit(Application.status)