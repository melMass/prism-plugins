import logging
import os
import platform
import subprocess

from PrismUtils.Decorators import err_catcher_plugin as err_catcher
from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

logger = logging.getLogger(__name__)


class Prism_SynthEyes_externalAccess_Functions(object):
    def __init__(self, core, plugin):
        self.core = core
        self.plugin = plugin
        self.core.registerCallback(
            "getIconPathForFileType", self.getIconPathForFileType, plugin=self.plugin
        )

        # self.core.registerCallback(
        #     "openPBFileContextMenu", self.openPBFileContextMenu, plugin=self.plugin
        # )
        self.core.registerCallback(
            "mediaPlayerContextMenuRequested",
            self.mediaPlayerContextMenuRequested,
            plugin=self.plugin,
        )

        self.initializeFirstLaunch()
        self.initialize()

    @err_catcher(name=__name__)
    def initializeFirstLaunch(self):
        if not self.core.uiAvailable:
            return

        if self.core.getConfig("syntheyes", "initialized", config="user"):
            return

        if self.core.getConfig("dccoverrides", "SynthEyes_path"):
            return

        msg = 'Please specify the "SynthEyes" executable to use the "SynthEyes" plugin in Prism.\nYou can change the path to the executable later in the "DCC Apps" tab of the Prism User Settings.'
        result = self.core.popupQuestion(
            msg, buttons=["Browse...", "Cancel"], icon=QMessageBox.Information
        )

        if result == "Browse...":
            if platform.system() == "Windows":
                fStr = "Executable (*.exe)"
            else:
                fStr = "All files (*)"

            windowTitle = "Select PureRef executable"
            selectedPath = QFileDialog.getOpenFileName(
                self.core.messageParent, windowTitle, self.core.prismRoot, fStr
            )[0]

            if not selectedPath:
                return

            cData = {
                "dccoverrides": {
                    "SynthEyes_override": True,
                    "SynthEyes_path": selectedPath,
                }
            }

            self.core.setConfig(data=cData, config="user")

        self.core.setConfig("syntheyes", "initialized", True, config="user")

    @err_catcher(name=__name__)
    def initialize(self):
        if hasattr(self.core, "pb") and self.core.pb:
            self.core.pb.sceneBrowser.appFilters[self.pluginName] = {
                "formats": self.sceneFormats,
                "show": True,
            }
            self.core.pb.sceneBrowser.refreshScenefiles()

    @err_catcher(name=__name__)
    def preUninstall(self):
        self.core.setConfig("syntheyes", "initialized", delete=True, config="user")
        self.core.setConfig(
            "dccoverrides", "SynthEyes_override", delete=True, config="user"
        )
        self.core.setConfig(
            "dccoverrides", "SynthEyes_path", delete=True, config="user"
        )

    @err_catcher(name=__name__)
    def getPresetScenes(self, presetScenes):
        presetDir = os.path.join(self.pluginDirectory, "Presets")
        scenes = self.core.entities.getPresetScenesFromFolder(presetDir)
        presetScenes += scenes

    @err_catcher(name=__name__)
    def getIconPathForFileType(self, extension):
        if extension == ".sni":
            return self.appIcon

    # @err_catcher(name=__name__)
    # def openPBFileContextMenu(self, origin, menu, filepath):
    #     ext = os.path.splitext(filepath)[1]
    #     if ext == ".sni":
    #         pmenu = QMenu("SynthEyes", origin)

    #         data = self.core.entities.getScenefileData(filepath)
    #         entity = data.get("type")
    #         if entity:
    #             action = QAction("Set as %s preview" % entity, origin)
    #             # action.triggered.connect(lambda: self.setAsPreview(origin, filepath))
    #             pmenu.addAction(action)

    #             action = QAction("Export...", origin)
    #             # action.triggered.connect(lambda: self.exportDlg(filepath))
    #             pmenu.addAction(action)

    #         menu.insertMenu(menu.actions()[0], pmenu)

    @err_catcher(name=__name__)
    def mediaPlayerContextMenuRequested(self, origin, menu):
        if not type(origin.origin).__name__ == "MediaBrowser":
            return

        version = origin.origin.getCurrentVersion()
        if not version:
            return

        if not origin.seq:
            return

        filepath = origin.seq[0]
        if os.path.splitext(filepath)[1] in self.core.media.videoFormats:
            return

        action = QAction("Open in SynthEyes...", origin)
        action.triggered.connect(lambda: self.openMediaInSynthEyes(origin.seq))
        menu.insertAction(menu.actions()[-2], action)

    @err_catcher(name=__name__)
    def openMediaInSynthEyes(self, media):
        exe = None
        orApp = self.core.getConfig("dccoverrides", f"{self.pluginName}_override")
        if not orApp:
            msg = "Invalid executable specified. Please update the executable setting in the DCC apps tab in the Prism User Settings."
            self.core.popup(msg)
            return

        appOrPath = self.core.getConfig("dccoverrides", f"{self.pluginName}_path")
        if appOrPath and os.path.exists(appOrPath):
            exe = appOrPath
        else:
            msg = "Invalid executable specified. Please update the executable setting in the DCC apps tab in the Prism User Settings."
            self.core.popup(msg)
            return

        args = [exe] + media
        subprocess.Popen(args)
