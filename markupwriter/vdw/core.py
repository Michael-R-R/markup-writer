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
    StartupParser,
)

from markupwriter.config import (
    AppConfig,
    ProjectConfig,
)

from markupwriter.common.util import (
    File,
    Serialize,
)

import markupwriter.vdw.delegate as d


class CoreData(QObject):
    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)

        self.mmbd = d.MainMenuBarDelegate(self)
        self.cwd = d.CentralWidgetDelegate(self)
        self.dtd = d.DocumentTreeDelegate(self)
        self.ded = d.DocumentEditorDelegate(self)
        self.dpd = d.DocumentPreviewDelegate(self)

    def setup(self, mwd: d.MainWindowDelegate):
        mwd.worker.setMenuBar(self.mmbd.view)
        mwd.worker.setCentralWidget(self.cwd.view)

        cww = self.cwd.worker
        cww.insertWidgetLHS(0, self.dtd.view)
        cww.insertWidgetRHS(0, self.ded.view)
        cww.addWidgetRHS(self.dpd.view)
        
        self.mmbd.setup()
        self.cwd.setup()
        self.dtd.setup()
        self.ded.setup()
        self.dpd.setup()

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
        self.data: CoreData = None

        self.setup(CoreData(self))

    def setup(self, data: CoreData):
        self.data = data

        self._setupCoreSlots()
        self._setupMainWindowWorkerSlots()
        self._setupMenuBarWorkerSlots()
        self._setupTreeWorkerSlots()
        self._setupEditorWorkerSlots()
        self._setupPreviewWorkerSlots()
        
        self.data.setup(self.mwd)

        self.setWindowTitle()

    def run(self):
        self.mwd.view.show()

    def reset(self):
        ProjectConfig.projectName = None
        ProjectConfig.dir = None
        self.setup(CoreData(self))

    def setWindowTitle(self):
        title = "{} - {}".format(AppConfig.APP_NAME, ProjectConfig.projectName)
        self.mwd.worker.setWindowTitle(title)

    def _setupCoreSlots(self):
        mwd = self.mwd
        mwd.viewClosing.connect(self._onAppClosing)

        mmbd = self.data.mmbd
        mmbd.fmNewTriggered.connect(self._onNewProject)
        mmbd.fmOpenTriggered.connect(self._onOpenProject)
        mmbd.fmSaveDocTriggered.connect(self._onSaveDocument)
        mmbd.fmSaveTriggered.connect(self._onSaveProject)
        mmbd.fmSaveAsTriggered.connect(self._onSaveAsProject)
        mmbd.fmCloseTriggered.connect(self._onCloseProject)
        mmbd.fmExitTriggered.connect(self._onExit)
        
    def _setupMainWindowWorkerSlots(self):
        pass

    def _setupMenuBarWorkerSlots(self):
        worker = self.data.mmbd.worker
        
        ded = self.data.ded
        ded.docStatusChanged.connect(worker.onDocumentStatusChanged)
        
        dpd = self.data.dpd
        dpd.tabCountChanged.connect(worker.onTabCountChanged)

    def _setupTreeWorkerSlots(self):
        worker = self.data.dtd.worker
        
        mmbd = self.data.mmbd
        mmbd.fmImportTxtTriggered.connect(worker.onImportTxtFile)
        mmbd.fmExportTriggered.connect(worker.onExportNovel)
        mmbd.vmDocTreeTriggered.connect(worker.onFocusTreeTriggered)
        mmbd.vmTelescopeTriggered.connect(worker.onTelescopeTriggered)

        dtd = self.data.dtd
        dtd.fileAdded.connect(worker.onFileAdded)
        dtd.fileRemoved.connect(worker.onFileRemoved)
        dtd.dragDropDone.connect(worker.onDragDropDone)
        dtd.contextMenuRequested.connect(worker.onContextMenuRequested)
        dtd.navUpClicked.connect(worker.onNavItemUp)
        dtd.navDownClicked.connect(worker.onNavItemDown)
        dtd.cmPreviewClicked.connect(worker.onPreviewItem)
        dtd.cmRenameClicked.connect(worker.onRenamedItem)
        dtd.cmToTrashClicked.connect(worker.onTrashItem)
        dtd.cmRecoverClicked.connect(worker.onRecoverItem)
        dtd.cmEmptyTrashClicked.connect(worker.onEmptyTrash)
        dtd.createNovelClicked.connect(worker.onNovelFolderCreated)
        dtd.createFolderClicked.connect(worker.onMiscFolderCreated)
        dtd.createTitleClicked.connect(worker.onTitleFileCreated)
        dtd.createChapterClicked.connect(worker.onChapterFileCreated)
        dtd.createSceneClicked.connect(worker.onSceneFileCreated)
        dtd.createSectionClicked.connect(worker.onSectionFileCreated)
        dtd.createFileClicked.connect(worker.onMiscFileCreated)

        ded = self.data.ded
        ded.wordCountChanged.connect(worker.onWordCountChanged)
        ded.refPreviewRequested.connect(worker.onRefPreviewRequested)

    def _setupEditorWorkerSlots(self):
        worker = self.data.ded.worker
        
        mmbd = self.data.mmbd
        mmbd.dmSpellToggled.connect(worker.onSpellToggled)
        mmbd.vmDocEditorTriggered.connect(worker.onFocusEditorTriggered)

        dtd = self.data.dtd
        dtd.fileOpened.connect(worker.onFileOpened)
        dtd.fileRemoved.connect(worker.onFileRemoved)
        dtd.fileMoved.connect(worker.onFileMoved)
        dtd.fileRenamed.connect(worker.onFileRenamed)

        ded = self.data.ded
        ded.stateChanged.connect(worker.onStateChanged)
        ded.stateBufferChanged.connect(worker.onStateBufferChanged)
        ded.closeDocClicked.connect(worker.onCloseDocument)
        ded.showRefPopupClicked.connect(worker.onShowRefPopupClicked)
        ded.showRefPreviewClicked.connect(worker.onShowRefPreviewClicked)
        ded.editorResized.connect(worker.onEditorResized)
        ded.contextMenuRequested.connect(worker.onContxtMenuRequested)
        ded.showSearchTriggered.connect(worker.onSearchTriggered)
        ded.searchChanged.connect(worker.onSearchChanged)
        ded.nextSearchClicked.connect(worker.onNextSearch)
        ded.prevSearchCliced.connect(worker.onPrevSearch)
        ded.replaceClicked.connect(worker.onReplaceSearch)
        ded.replaceAllClicked.connect(worker.onReplaceAllSearch)
        ded.closeSearchClicked.connect(worker.onSearchTriggered)

    def _setupPreviewWorkerSlots(self):
        worker = self.data.dpd.worker
        
        mmbd = self.data.mmbd
        mmbd.vmDocPreviewTriggered.connect(worker.onFocusPreviewTriggered)
        mmbd.dmRefreshPreview.connect(worker.onRefreshTriggered)
        mmbd.dmTogglePreview.connect(worker.onToggleTriggered)

        dtd = self.data.dtd
        dtd.fileRemoved.connect(worker.onFileRemoved)
        dtd.fileRenamed.connect(worker.onFileRenamed)
        dtd.previewRequested.connect(worker.onFilePreviewed)

        dpd = self.data.dpd
        dpd.closeTabRequested.connect(worker.onCloseTabRequested)

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

        self.data.mmbd.worker.onNewProject()
        self.data.dtd.worker.onNewProject()

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

        data = CoreData(self)
        self.setup(data)
        
        data = Serialize.existRead(data, ProjectConfig.filePath())
        if data is None:
            self.reset()
            return

        self.data.mmbd.worker.onOpenProject()
        self.data.dtd.worker.onOpenProject()

        te = self.data.ded.view.textEdit
        StartupParser.run(te.refManager)

        self.mwd.worker.showStatusBarMsg("Project opened...", 1500)

    @pyqtSlot()
    def _onSaveDocument(self):
        if self.data.ded.worker.onSaveDocument():
            self.mwd.worker.showStatusBarMsg("Document saved...", 1500)

    @pyqtSlot()
    def _onSaveProject(self):
        if not ProjectConfig.hasActiveProject():
            return False

        self._onSaveDocument()

        if not Serialize.write(ProjectConfig.filePath(), self.data):
            return False
            
        self.mwd.worker.showStatusBarMsg("Project saved...", 1500)
            
        return True

    @pyqtSlot()
    def _onSaveAsProject(self):
        if ProjectHelper.askToSave(self.mwd.view):
            self._onSaveProject()

        pair = ProjectHelper.mkProjectDir(self.mwd.view)
        if pair == (None, None):
            self.reset()
            return
        
        srcContentPath = ProjectConfig.contentPath()
        if srcContentPath is None:
            self.reset()
            return

        ProjectConfig.projectName = pair[0]
        ProjectConfig.dir = pair[1]

        if not self._onSaveProject():
            self.reset()
            return
        
        dstContentPath = ProjectConfig.contentPath()
        if not File.cpdir(srcContentPath, dstContentPath):
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

    @pyqtSlot()
    def _onAppClosing(self):
        self._onSaveProject()
