#!/usr/bin/python

import os
import sys

# Check for dependacies
try:
    import PyQt6.QtCore
    import PyQt6.QtWidgets
    import PyQt6.QtGui
except Exception as e:
    print(str(e))
    sys.exit(1)
    
# Set Windows app id
try:
    from ctypes import windll
    
    myappid = "michaelrule.markupwriter.version 0.1.0"
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

if __name__ == "__main__":
    from markupwriter.application import (
    Application,
)
    wd = os.path.dirname(__file__)
    
    Application.start(wd)
    Application.run(sys.argv[1:])
    Application.close()

    sys.exit(Application.status)