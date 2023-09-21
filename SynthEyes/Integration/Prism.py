import logging
import os
import subprocess
import sys

logger = logging.getLogger(__name__)


prismRoot = os.getenv("PRISM_ROOT")
if not prismRoot:
    prismRoot = "$PRISMROOT$"

if sys.version_info[0] != 3 or sys.version_info[1] != 9:

    def log_subprocess_output(pipe):
        for line in iter(pipe.readline, b""):  # b'\n'-separated lines
            print((line.rstrip().decode()))

    executable = os.path.join(prismRoot, "Python39", "Prism.exe")
    p = subprocess.Popen(
        [executable, sys.argv[0]], stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    with p.stdout:
        log_subprocess_output(p.stdout)

    sys.exit(0)

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel("INFO")
logger.info("loading Prism")

sys.path.append(os.path.join(prismRoot, "Scripts"))
sys.path.append(os.path.join(prismRoot, "PythonLibs", "Python39"))
sys.path.append(os.path.join(prismRoot, "PythonLibs", "Python3", "PySide"))

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtCore import *
    from PySide.QtGui import *

qapp = QApplication.instance()
if qapp is None:
    qapp = QApplication(sys.argv)

import PrismCore

pcore = PrismCore.create(app="Resolve", prismArgs=["noProjectBrowser"])
qapp.exec_()

logger.info("finished Prism execution")
