#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
    QDataStream,
    pyqtSlot,
)

from PyQt6.QtWidgets import (
    QApplication,
)

from markupwriter.support.core import (
    ProjectHelper,
    EpubExporter,
    StartupParser,
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
        self.mmbw = None
        self.dtw = None
        self.dew = None

        self.setup(CoreData(self))

    def setup(self, data: CoreData):
        self.data = data
        self.data.setup(self.mwd)

        self.mmbw = w.MainMenuBarWorker(self.data.mmbd, self)
        self.dtw = w.DocumentTreeWorker(self.data.dtd, self)
        self.dew = w.DocumentEditorWorker(self.data.ded, self)
        self.dpw = w.DocumentPreviewWorker(self.data.dpd, self)

        self._setupCoreSlots()
        self._setupMenuBarWorkerSlots()
        self._setupTreeWorkerSlots()
        self._setupEditorWorkerSlots()
        self._setupPreviewWorkerSlots()

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
        self.mwd.viewClosing.connect(self._onAppClosing)

        self.data.mmbd.fmNewTriggered.connect(self._onNewProject)
        self.data.mmbd.fmOpenTriggered.connect(self._onOpenProject)
        self.data.mmbd.fmSaveTriggered.connect(self._onSaveProject)
        self.data.mmbd.fmSaveAsTriggered.connect(self._onSaveAsProject)
        self.data.mmbd.fmExportTriggered.connect(self._onExport)
        self.data.mmbd.fmCloseTriggered.connect(self._onCloseProject)
        self.data.mmbd.fmExitTriggered.connect(self._onExit)

    def _setupMenuBarWorkerSlots(self):
        self.data.ded.docStatusChanged.connect(self.mmbw.onDocumentStatusChanged)

    def _setupTreeWorkerSlots(self):
        self.data.dtd.fileAdded.connect(self.dtw.onFileAdded)
        self.data.dtd.fileRemoved.connect(self.dtw.onFileRemoved)
        self.data.dtd.dragDropDone.connect(self.dtw.onDragDropDone)
        self.data.dtd.navUpClicked.connect(self.dtw.onNavItemUp)
        self.data.dtd.navDownClicked.connect(self.dtw.onNavItemDown)
        self.data.dtd.cmPreviewClicked.connect(self.dtw.onPreviewItem)
        self.data.dtd.cmRenameClicked.connect(self.dtw.onRenamedItem)
        self.data.dtd.cmToTrashClicked.connect(self.dtw.onTrashItem)
        self.data.dtd.cmRecoverClicked.connect(self.dtw.onRecoverItem)
        self.data.dtd.cmEmptyTrashClicked.connect(self.dtw.onEmptyTrash)
        self.data.dtd.createNovelClicked.connect(self.dtw.onNovelFolderCreated)
        self.data.dtd.createFolderClicked.connect(self.dtw.onMiscFolderCreated)
        self.data.dtd.createTitleClicked.connect(self.dtw.onTitleFileCreated)
        self.data.dtd.createChapterClicked.connect(self.dtw.onChapterFileCreated)
        self.data.dtd.createSceneClicked.connect(self.dtw.onSceneFileCreated)
        self.data.dtd.createSectionClicked.connect(self.dtw.onSectionFileCreated)
        self.data.dtd.createFileClicked.connect(self.dtw.onMiscFileCreated)

        self.data.ded.wordCountChanged.connect(self.dtw.onWordCountChanged)
        self.data.ded.docPreviewRequested.connect(self.dtw.onDocPreviewRequested)

    def _setupEditorWorkerSlots(self):
        self.data.mmbd.fmSaveDocTriggered.connect(self.dew.onSaveDocument)
        
        self.data.dtd.fileOpened.connect(self.dew.onFileOpened)
        self.data.dtd.fileRemoved.connect(self.dew.onFileRemoved)
        self.data.dtd.fileMoved.connect(self.dew.onFileMoved)
        self.data.dtd.fileRenamed.connect(self.dew.onFileRenamed)

        self.data.ded.closeDocClicked.connect(self.dew.onCloseDocument)
        self.data.ded.refPopupTriggered.connect(self.dew.onRefPopupTriggered)
        self.data.ded.refPreviewTriggered.connect(self.dew.onRefPreviewTriggered)
        self.data.ded.editorResized.connect(self.dew.onEditorResized)
        self.data.ded.showSearchTriggered.connect(self.dew.onSearchTriggered)
        self.data.ded.searchChanged.connect(self.dew.onSearchChanged)
        self.data.ded.nextSearchClicked.connect(self.dew.onNextSearch)
        self.data.ded.prevSearchCliced.connect(self.dew.onPrevSearch)
        self.data.ded.replaceClicked.connect(self.dew.onReplaceSearch)
        self.data.ded.replaceAllClicked.connect(self.dew.onReplaceAllSearch)
        self.data.ded.closeSearchClicked.connect(self.dew.onSearchTriggered)

    def _setupPreviewWorkerSlots(self):
        self.data.dtd.fileRemoved.connect(self.dpw.onFileRemoved)
        self.data.dtd.fileRenamed.connect(self.dpw.onFileRenamed)
        self.data.dtd.previewRequested.connect(self.dpw.onFilePreviewed)

        # TODO somehow get text editor priview request

        self.data.dpd.closeTabRequested.connect(self.dpw.onCloseTabRequested)

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

        self.mmbw.onNewProject()
        self.dtw.onNewProject()

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

        self.mmbw.onOpenProject()
        self.dtw.onOpenProject()

        refManager = self.dew.refManager
        StartupParser.run(refManager)

    @pyqtSlot()
    def _onSaveDocument(self):
        self.dew.onSaveDocument()

    @pyqtSlot()
    def _onSaveProject(self):
        if not ProjectConfig.hasActiveProject():
            return False

        self._onSaveDocument()

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
    def _onExport(self):
        tw = self.data.dtd.view.treeWidget
        
        exporter = EpubExporter()
        exporter.export(tw, self.mwd.view)

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

    @pyqtSlot()
    def _onAppClosing(self):
        self._onSaveProject()
