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
        
        dts = AppConfig.docTreeSize
        des = AppConfig.docEditorSize
        dps = AppConfig.docPreviewSize
        self.cwd.setSizesLHS([dts.width(), des.width() + dps.width()])
        self.cwd.setSizesRHS([des.width(), dps.width()])

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

        self.mww = w.MainWindowWorker(self.mwd, self)
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
        self.mwd.setWindowTitle(title)

    def _setupCoreSlots(self):
        self.mwd.viewClosing.connect(self._onAppClosing)

        mmbd = self.data.mmbd
        mmbd.fmNewTriggered.connect(self._onNewProject)
        mmbd.fmOpenTriggered.connect(self._onOpenProject)
        mmbd.fmSaveDocTriggered.connect(self._onSaveDocument)
        mmbd.fmSaveTriggered.connect(self._onSaveProject)
        mmbd.fmSaveAsTriggered.connect(self._onSaveAsProject)
        mmbd.fmExportTriggered.connect(self._onExport)
        mmbd.fmCloseTriggered.connect(self._onCloseProject)
        mmbd.fmExitTriggered.connect(self._onExit)

    def _setupMenuBarWorkerSlots(self):
        ded = self.data.ded
        ded.docStatusChanged.connect(self.mmbw.onDocumentStatusChanged)

    def _setupTreeWorkerSlots(self):
        dtd = self.data.dtd
        dtd.fileAdded.connect(self.dtw.onFileAdded)
        dtd.fileRemoved.connect(self.dtw.onFileRemoved)
        dtd.dragDropDone.connect(self.dtw.onDragDropDone)
        dtd.navUpClicked.connect(self.dtw.onNavItemUp)
        dtd.navDownClicked.connect(self.dtw.onNavItemDown)
        dtd.filterChanged.connect(self.dtw.onFilterTextChanged)
        dtd.cmPreviewClicked.connect(self.dtw.onPreviewItem)
        dtd.cmRenameClicked.connect(self.dtw.onRenamedItem)
        dtd.cmToTrashClicked.connect(self.dtw.onTrashItem)
        dtd.cmRecoverClicked.connect(self.dtw.onRecoverItem)
        dtd.cmEmptyTrashClicked.connect(self.dtw.onEmptyTrash)
        dtd.createNovelClicked.connect(self.dtw.onNovelFolderCreated)
        dtd.createFolderClicked.connect(self.dtw.onMiscFolderCreated)
        dtd.createTitleClicked.connect(self.dtw.onTitleFileCreated)
        dtd.createChapterClicked.connect(self.dtw.onChapterFileCreated)
        dtd.createSceneClicked.connect(self.dtw.onSceneFileCreated)
        dtd.createSectionClicked.connect(self.dtw.onSectionFileCreated)
        dtd.createFileClicked.connect(self.dtw.onMiscFileCreated)

        ded = self.data.ded
        ded.wordCountChanged.connect(self.dtw.onWordCountChanged)
        ded.docPreviewRequested.connect(self.dtw.onDocPreviewRequested)

    def _setupEditorWorkerSlots(self):
        dtd = self.data.dtd
        dtd.fileOpened.connect(self.dew.onFileOpened)
        dtd.fileRemoved.connect(self.dew.onFileRemoved)
        dtd.fileMoved.connect(self.dew.onFileMoved)
        dtd.fileRenamed.connect(self.dew.onFileRenamed)

        ded = self.data.ded
        ded.closeDocClicked.connect(self.dew.onCloseDocument)
        ded.refPopupTriggered.connect(self.dew.onRefPopupTriggered)
        ded.refPreviewTriggered.connect(self.dew.onRefPreviewTriggered)
        ded.editorResized.connect(self.dew.onEditorResized)
        ded.showSearchTriggered.connect(self.dew.onSearchTriggered)
        ded.searchChanged.connect(self.dew.onSearchChanged)
        ded.nextSearchClicked.connect(self.dew.onNextSearch)
        ded.prevSearchCliced.connect(self.dew.onPrevSearch)
        ded.replaceClicked.connect(self.dew.onReplaceSearch)
        ded.replaceAllClicked.connect(self.dew.onReplaceAllSearch)
        ded.closeSearchClicked.connect(self.dew.onSearchTriggered)

    def _setupPreviewWorkerSlots(self):
        dtd = self.data.dtd
        dtd.fileRemoved.connect(self.dpw.onFileRemoved)
        dtd.fileRenamed.connect(self.dpw.onFileRenamed)
        dtd.previewRequested.connect(self.dpw.onFilePreviewed)

        dpd = self.data.dpd
        dpd.closeTabRequested.connect(self.dpw.onCloseTabRequested)

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

        data: CoreData = Serialize.readFromFile(CoreData, ProjectConfig.filePath())
        if data is None:
            self.reset()
            return

        self.setup(data)

        self.mmbw.onOpenProject()
        self.dtw.onOpenProject()

        refManager = self.dew.refManager
        StartupParser.run(refManager)
        
        self.mww.showStatusBarMsg("Project opened...", 1500)

    @pyqtSlot()
    def _onSaveDocument(self):
        if self.dew.onSaveDocument():
            self.mww.showStatusBarMsg("Document saved...", 1500)

    @pyqtSlot()
    def _onSaveProject(self):
        if not ProjectConfig.hasActiveProject():
            return False

        self._onSaveDocument()

        if Serialize.writeToFile(ProjectConfig.filePath(), self.data):
            self.mww.showStatusBarMsg("Project saved...", 1500)

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
        
        self.mww.showStatusBarMsg("Novel exported...", 1500)

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
