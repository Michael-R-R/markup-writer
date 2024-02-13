#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    QDataStream,
    pyqtSlot,
)

from PyQt6.QtWidgets import (
    QApplication,
)

from markupwriter.support.mainwindow import (
    ProjectHelper,
)

from markupwriter.config import (
    AppConfig,
    ProjectConfig,
)

from markupwriter.common.util import (
    Serialize,
)

import markupwriter.mv.delegate as d
import markupwriter.mv.worker as w


class CoreData(QObject):
    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)

        self.mmbd = d.MainMenuBarDelegate(self)
        self.cwd = d.CentralWidgetDelegate(self)
        self.dtd = d.DocumentTreeDelegate(self)
        self.ded = d.DocumentEditorDelegate(self)
        self.dpd = d.DocumentPreviewDelegate(self)

    def setup(self, mwd: d.MainWindowDelegate):
        mwd.setMenuBar(self.mmbd.view)
        mwd.setCentralWidget(self.cwd.view)

        self.cwd.insertWidgetLHS(0, self.dtd.view)
        self.cwd.insertWidgetRHS(0, self.ded.view)
        self.cwd.addWidgetRHS(self.dpd.view)

    def __rlshift__(self, sout: QDataStream) -> QDataStream:
        sout << self.mmbd
        sout << self.cwd
        sout << self.dtd
        sout << self.ded
        sout << self.dpd
        return sout

    def __rrshift__(self, sin: QDataStream) -> QDataStream:
        sin >> self.mmbd
        sin >> self.cwd
        sin >> self.dtd
        sin >> self.ded
        sin >> self.dpd
        return sin


class Core(QObject):
    def __init__(self, parent: QObject | None) -> None:
        super().__init__(parent)

        self.mwd = d.MainWindowDelegate(self)
        self.data = None
        
        self.setup(CoreData(self))

    def setup(self, data: CoreData):
        self.data = data
        self.data.setup(self.mwd)
        
        self._setupCoreSlots()
        
        self.setWindowTitle()

    def run(self):
        self.mwd.showMainView()
        
    def reset(self):
        ProjectConfig.projectName = None
        ProjectConfig.dir = None
        self.setup(CoreData(self))

    def setWindowTitle(self):
        title = "{} - {}".format(AppConfig.APP_NAME, ProjectConfig.projectName)
        self.mwd.setViewTitle(title)

    def _setupCoreSlots(self):
        self.data.mmbd.fmNewTriggered.connect(self._onNewProject)
        self.data.mmbd.fmOpenTriggered.connect(self._onOpenProject)
        self.data.mmbd.fmSaveTriggered.connect(self._onSaveProject)
        self.data.mmbd.fmSaveAsTriggered.connect(self._onSaveAsProject)
        self.data.mmbd.fmCloseTriggered.connect(self._onCloseProject)
        self.data.mmbd.fmExitTriggered.connect(self._onExit)

    @pyqtSlot()
    def _onNewProject(self):
        if not self._onCloseProject():
            return

        info = ProjectHelper.mkProjectDir(self.mwd.view)
        if info == (None, None):
            return

        ProjectConfig.projectName = info[0]
        ProjectConfig.dir = info[1]

        self.setup(CoreData(self))

        data = self.data
        data.mmbd.setEnableSaveAction(True)
        data.mmbd.setEnableSaveAsAction(True)
        data.mmbd.setEnableExportAction(True)
        data.mmbd.setEnableCloseAction(True)

        data.dtd.setEnabledTreeBarActions(True)
        data.dtd.setEnabledTreeActions(True)
        data.dtd.createRootFolders()

        self._onSaveProject()

    @pyqtSlot()
    def _onOpenProject(self):
        if not self._onCloseProject():
            return

        info = ProjectHelper.openProjectPath(self.mwd.view)
        if info == (None, None):
            return
        
        ProjectConfig.projectName = info[0]
        ProjectConfig.dir = info[1]

        data: CoreData = Serialize.read(CoreData, ProjectConfig.filePath())
        if data is None:
            self.reset()
            return

        self.setup(data)

        data.mmbd.setEnableSaveAction(True)
        data.mmbd.setEnableSaveAsAction(True)
        data.mmbd.setEnableExportAction(True)
        data.mmbd.setEnableCloseAction(True)

        data.dtd.setEnabledTreeBarActions(True)
        data.dtd.setEnabledTreeActions(True)
        
        # TODO do startup parser

    @pyqtSlot()
    def _onSaveProject(self):
        if not ProjectConfig.hasActiveProject():
            return False

        # TODO save opened document

        return Serialize.write(ProjectConfig.filePath(), self.data)

    @pyqtSlot()
    def _onSaveAsProject(self):
        if ProjectHelper.askToSave(self.mwd.view):
            self._onSaveProject()

        pair = ProjectHelper.mkProjectDir(self.mwd.view)
        if pair == (None, None):
            self.reset()
            return

        ProjectConfig.projectName = pair[0]
        ProjectConfig.dir = pair[1]

        if not self._onSaveProject():
            self.reset()
            return

        self.setWindowTitle()

    @pyqtSlot()
    def _onCloseProject(self):
        if not ProjectConfig.hasActiveProject():
            return True

        if not ProjectHelper.askToSaveClose(self.mwd.view):
            return False

        self._onSaveProject()
        self.reset()

        return True

    @pyqtSlot()
    def _onExit(self):
        if ProjectHelper.askToExit(self.mwd.view):
            self._onSaveProject()
            QApplication.quit()