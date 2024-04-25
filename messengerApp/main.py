import sys

import qdarkstyle
from PyQt5.QtWidgets import QApplication

from mess_interface import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    stylesheet = qdarkstyle.load_stylesheet_pyqt5()
    app.setStyleSheet(stylesheet)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
