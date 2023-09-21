import os
import platform
import sys

from PrismUtils.Decorators import err_catcher_plugin as err_catcher
from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *


class Prism_SynthEyes_Integration(object):
    def __init__(self, core, plugin):
        self.core = core
        self.plugin = plugin

        if platform.system() == "Windows":
            self.examplePath = os.path.join(
                os.environ["APPDATA"], "SynthEyes", "scripts"
            )

    @err_catcher(name=__name__)
    def getExecutable(self):
        execPath = ""
        if platform.system() == "Windows":
            execPath = "C:\\Program Files\\Andersson Technologies LLC\\SynthEyes\\SynthEyes64.exe"

        return execPath

    def addIntegration(self, installPath):
        try:
            if not os.path.exists(installPath):
                msg = "Invalid Resolve path: %s.\nThe path doesn't exist." % installPath
                self.core.popup(msg)
                return False

            if os.path.basename(installPath) not in ["scripts"]:
                msg = (
                    'The Prism integration needs to be installed to the SynthEyes user scripts folder, but the selected folder doesn\'t end with "/scripts". Are you sure you want to continue?\n\n%s'
                    % installPath
                )
                result = self.core.popupQuestion(msg, icon=QMessageBox.Warning)
                if result == "No":
                    return

            integrationBase = os.path.join(self.pluginDirectory, "Integration")

            cmds = []
            for filename in ["Prism.py"]:
                origFile = os.path.join(integrationBase, filename)
                targetFile = os.path.join(installPath, filename)

                if os.path.exists(targetFile):
                    cmd = {
                        "type": "removeFile",
                        "args": [targetFile],
                        "validate": False,
                    }
                    cmds.append(cmd)

                cmd = {"type": "copyFile", "args": [origFile, targetFile]}
                cmds.append(cmd)

                with open(origFile, "r") as init:
                    initStr = init.read()

                prism_root = self.core.prismRoot.replace("\\", "/")
                initStr = initStr.replace("$PRISMROOT$", f"{prism_root}")

                cmd = {"type": "writeToFile", "args": [targetFile, initStr]}
                cmds.append(cmd)

            result = self.core.runFileCommands(cmds)
            if result is True:
                return True
            elif result is False:
                return False
            else:
                raise Exception(result)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            msgStr = (
                "Errors occurred during the installation of the Resolve integration.\nThe installation is possibly incomplete.\n\n%s\n%s\n%s"
                % (str(e), exc_type, exc_tb.tb_lineno)
            )

            self.core.popup(msgStr)
            return False

    @err_catcher(name=__name__)
    def removeIntegration(self, installPath):
        pFiles = []
        path = os.path.join(installPath, "Prism.py")
        pFiles.append(path)

        cmds = []
        for filepath in pFiles:
            if os.path.exists(filepath):
                cmd = {"type": "removeFile", "args": [filepath]}
                cmds.append(cmd)

        result = self.core.runFileCommands(cmds)
        if result is True:
            return True
        elif result is False:
            return False
        else:
            raise Exception(result)

    @err_catcher(name=__name__)
    def updateInstallerUI(self, userFolders, pItem):
        pluginItem = QTreeWidgetItem([self.plugin.pluginName])
        pItem.addChild(pluginItem)

        pluginPath = self.examplePath

        if pluginPath and os.path.exists(pluginPath):
            pluginItem.setCheckState(0, Qt.Checked)
            pluginItem.setText(1, pluginPath)
            pluginItem.setToolTip(0, pluginPath)
        else:
            pluginItem.setCheckState(0, Qt.Unchecked)
            pluginItem.setText(1, "< doubleclick to browse path >")

    def installerExecute(self, item, result):
        try:
            installLocs = []

            if item.checkState(0) == Qt.Checked and os.path.exists(item.text(1)):
                result["SynthEyes integration"] = self.core.integration.addIntegration(
                    self.plugin.pluginName, path=item.text(1), quiet=True
                )
                if result["SynthEyes integration"]:
                    installLocs.append(item.text(1))

            return installLocs
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            msg = (
                "Errors occurred during the installation.\n The installation is possibly incomplete.\n\n%s\n%s\n%s\n%s"
                % (__file__, str(e), exc_type, exc_tb.tb_lineno)
            )
            self.core.popup(msg)
            return False
