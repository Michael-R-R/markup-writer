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

import markupwriter.vdw.delegate as d
import markupwriter.vdw.worker as w


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
        self.dtw = None
        self.dew = None

        self.setup(CoreData(self))

    def setup(self, data: CoreData):
        self.data = data
        self.data.setup(self.mwd)

        self.dtw = w.DocumentTreeWorker(self.data.dtd, self)
        self.dew = w.DocumentEditorWorker(self.data.ded, self)

        self._setupCoreSlots()
        self._setupTreeWorkerSlots()
        self._setupEditorWorkerSlots()

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

    def _setupTreeWorkerSlots(self):
        self.data.dtd.fileAdded.connect(self.dtw.onFileAdded)
        self.data.dtd.fileRemoved.connect(self.dtw.onFileRemoved)
        self.data.dtd.dragDropDone.connect(self.dtw.onDragDropDone)
        self.data.dtd.navedUpItem.connect(self.dtw.onNavItemUp)
        self.data.dtd.navedDownItem.connect(self.dtw.onNavItemDown)
        self.data.dtd.renamedItem.connect(self.dtw.onRenamedItem)
        self.data.dtd.trashedItem.connect(self.dtw.onTrashItem)
        self.data.dtd.recoveredItem.connect(self.dtw.onRecoverItem)
        self.data.dtd.emptiedTrash.connect(self.dtw.onEmptyTrash)
        self.data.dtd.createdNovel.connect(self.dtw.onNovelFolderCreated)
        self.data.dtd.createdMiscFolder.connect(self.dtw.onMiscFolderCreated)
        self.data.dtd.createdTitle.connect(self.dtw.onTitleFileCreated)
        self.data.dtd.createdChapter.connect(self.dtw.onChapterFileCreated)
        self.data.dtd.createdScene.connect(self.dtw.onSceneFileCreated)
        self.data.dtd.createdSection.connect(self.dtw.onSectionFileCreated)
        self.data.dtd.createdMiscFile.connect(self.dtw.onMiscFileCreated)

    def _setupEditorWorkerSlots(self):
        self.data.mmbd.fmSaveDocTriggered.connect(self.dew.onSaveDocument)
        self.data.mmbd.fmSaveTriggered.connect(self.dew.onSaveDocument)
        
        self.data.dtd.fileOpened.connect(self.dew.onFileOpened)
        self.data.dtd.fileRemoved.connect(self.dew.onFileRemoved)
        self.data.dtd.fileMoved.connect(self.dew.onFileMoved)
        self.data.dtd.fileRenamed.connect(self.dew.onFileRenamed)
        
        self.data.ded.closeDocClicked.connect(self.dew.onCloseDocument)

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
