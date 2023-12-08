#!/usr/bin/python

import sys

try:
    import PyQt6.QtCore
    import PyQt6.QtWidgets
    import PyQt6.QtGui
except Exception:
    print("ERROR::markupWriter::cannot import PyQt6 dependecies")

if __name__ == "__main__":
    from markupwriter.core import application
    application.run(sys.argv[1:])