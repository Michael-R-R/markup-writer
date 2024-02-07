#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    pyqtSlot,
)

from PyQt6.QtWidgets import (
    QApplication,
)

from markupwriter.mvc.model.core import (
    MainWindow,
)

from markupwriter.mvc.view.core import (
    MainWindowView,
)

from markupwriter.support.mainwindow import (
    ProjectHelper,
    StartupParser,
    ExportHelper,
)

from markupwriter.config import (
    AppConfig,
)

from markupwriter.common.util import (
    Serialize,
)


class MainWindowController(QObject):
    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)

        self.model = MainWindow(self)
        self.view = MainWindowView(None)

    def setup(self):
        self.model.menuBarController.setup()
        self.model.centralController.setup()
        self.model.statusBarController.setup()

        self.view.updateWindowTitle()
        self.view.setMenuBar(self.model.menuBarController.view)
        self.view.setCentralWidget(self.model.centralController.view)
        self.view.setStatusBar(self.model.statusBarController.view)

        # --- controllers --- #
        mbc = self.model.menuBarController
        cc = self.model.centralController
        dec = cc.model.docEditorController

        # --- main window controller slots --- #
        self.view.closing.connect(self._onSaveProject)
        mbc.newProjClicked.connect(self._onNewProject)
        mbc.openProjClicked.connect(self._onOpenProject)
        mbc.saveDocClicked.connect(self._onSaveDocument)
        mbc.saveProjClicked.connect(self._onSaveProject)
        mbc.saveProjAsClicked.connect(self._onSaveAsProject)
        mbc.exportClicked.connect(self._onExportProject)
        mbc.closeProjClicked.connect(self._onCloseProject)
        mbc.exitClicked.connect(self._onExit)
        
        # --- Menu controller slots --- #
        dec.hasOpenDocument.connect(mbc.setEnableSaveDocAction)

    def show(self):
        self.view.show()

    def reset(self):
        AppConfig.projectName = None
        AppConfig.projectDir = None
        self.model = MainWindow(self)
        self.setup()

    @pyqtSlot()
    def _onNewProject(self):
        if not self._onCloseProject():
            return

        pair = ProjectHelper.mkProjectDir(self.view)
        if pair == (None, None):
            return

        AppConfig.projectName = pair[0]
        AppConfig.projectDir = pair[1]

        self.model = MainWindow(self)
        self.setup()

        mbc = self.model.menuBarController
        mbc.setEnableSaveAction(True)
        mbc.setEnableSaveAsAction(True)
        mbc.setEnableExportAction(True)
        mbc.setEnableCloseAction(True)

        cc = self.model.centralController
        dtc = cc.model.docTreeController
        dtc.setEnabledTreeBarActions(True)
        dtc.setEnabledTreeActions(True)
        dtc.createRootFolders()

        self._onSaveProject()

        self.view.showStatusMsg("Project created...", 2000)

    @pyqtSlot()
    def _onOpenProject(self):
        if not self._onCloseProject():
            return

        pair = ProjectHelper.openProjectPath(self.view)
        if pair == (None, None):
            return

        AppConfig.projectName = pair[0]
        AppConfig.projectDir = pair[1]

        model: MainWindow = Serialize.read(MainWindow, AppConfig.projectFilePath())
        if model is None:
            self.reset()
            return

        self.model = model
        self.setup()

        mbc = self.model.menuBarController
        mbc.setEnableSaveAction(True)
        mbc.setEnableSaveAsAction(True)
        mbc.setEnableExportAction(True)
        mbc.setEnableCloseAction(True)

        cc = self.model.centralController
        dtc = cc.model.docTreeController
        dtc.setEnabledTreeBarActions(True)
        dtc.setEnabledTreeActions(True)
        
        StartupParser.run(cc)

        self.view.showStatusMsg("Project opened...", 2000)
        
    @pyqtSlot()
    def _onSaveDocument(self) -> bool:
        if not AppConfig.hasActiveProject():
            return False
        
        cc = self.model.centralController
        dec = cc.model.docEditorController
        if not dec.onSaveDocument():
            return False
        
        self.view.showStatusMsg("Document saved...", 2000)
        
        return True

    @pyqtSlot()
    def _onSaveProject(self) -> bool:
        if not AppConfig.hasActiveProject():
            return False
        if not Serialize.write(AppConfig.projectFilePath(), self.model):
            return False
        self._onSaveDocument()
        self.view.showStatusMsg("Project saved...", 2000)
        return True

    @pyqtSlot()
    def _onSaveAsProject(self):
        if ProjectHelper.askToSave(self.view):
            self._onSaveProject()

        pair = ProjectHelper.mkProjectDir(self.view)
        if pair == (None, None):
            self.reset()
            return

        AppConfig.projectName = pair[0]
        AppConfig.projectDir = pair[1]
        if not self._onSaveProject():
            self.reset()
            return

        self.view.updateWindowTitle()
        
    @pyqtSlot()
    def _onExportProject(self):
        cc = self.model.centralController
        dtc = cc.model.docTreeController
        
        ExportHelper.exportEPUB3(dtc, self.view)

    @pyqtSlot()
    def _onCloseProject(self) -> bool:
        if not AppConfig.hasActiveProject():
            return True

        if not ProjectHelper.askToSaveClose(self.view):
            return False

        self._onSaveProject()
        self.reset()

        return True

    @pyqtSlot()
    def _onExit(self):
        if ProjectHelper.askToExit(self.view):
            self._onSaveProject()
            QApplication.quit()
