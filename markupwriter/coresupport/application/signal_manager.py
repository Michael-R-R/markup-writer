#!/usr/bin/python

import markupwriter.core.main_window as mw
import markupwriter.core.central_widget as cw


class SignalManager(object):
    def setup(mainWindow: mw.MainWindow):
        SignalManager._mainWindow(mainWindow)
        SignalManager._treeView(mainWindow)
        SignalManager._editorView(mainWindow)

    def _mainWindow(window: mw.MainWindow):
        menubar = window.mainWidget.menuBar
        
        # --- File menu --- #
        fileMenu = menubar.fileMenu
        fileMenu.newAction.triggered.connect(window.onNewProject)
        fileMenu.openAction.triggered.connect(window.onOpenProject)
        fileMenu.saveAction.triggered.connect(window.onSaveProject)
        fileMenu.saveAsAction.triggered.connect(window.onSaveAsProject)
        fileMenu.closeAction.triggered.connect(window.onCloseProject)
        fileMenu.exitAction.triggered.connect(window.onExit)
        
    def _treeView(window: mw.MainWindow):
        treeview = window.mainWidget.treeView
        treebar = treeview.treeBar
        tree = treeview.tree
        
        # --- Tree bar --- #
        treebar.addItemAction.itemCreated.connect(treeview.onItemCreated)
        treebar.navUpAction.triggered.connect(treeview.onNavUpClicked)
        treebar.navDownAction.triggered.connect(treeview.onNavDownClicked)
        
        # --- Tree --- #
        tree.fileAdded.connect(treeview.onFileAdded)
        tree.fileRemoved.connect(treeview.onFileRemoved)

    def _editorView(window: mw.MainWindow):
        editorview = window.mainWidget.editorView
        
        # --- Tree --- #
        treeView = window.mainWidget.treeView
        tree = treeView.tree
        tree.fileAdded.connect(editorview.onFileAdded)
        tree.fileRemoved.connect(editorview.onFileRemoved)
        tree.fileMoved.connect(editorview.onFileMoved)
        tree.fileDoubleClicked.connect(editorview.onFileDoubleClicked)