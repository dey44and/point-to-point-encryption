import os

from PyQt5 import QtCore
from PyQt5.QtWidgets import (QWidget, QMainWindow)
from PyQt5.uic import loadUi


def debug_trace():
    from pdb import set_trace
    QtCore.pyqtRemoveInputHook()
    set_trace()
    # QtCore.pyqtRestoreInputHook()


class MainWindow(QMainWindow):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    def __init__(self):
        super(MainWindow, self).__init__()
        ui_path = os.path.join(self.ROOT_DIR, 'AppUI.ui')
        loadUi(ui_path, self)
