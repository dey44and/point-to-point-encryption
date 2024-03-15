import sys

import qdarkstyle
from PyQt5.QtWidgets import QApplication

from myLib import MyLib
from qtapp import MainWindow

import myLib.MyLib

if __name__ == '__main__':
    key = b"this is a very secret key!!!"
    rounds = 20
    rc6 = MyLib.RC6(key, rounds)

    plaintext = b"Hello, RC6 with CBC Mode!"
    iv = b"\x00" * 16


    encrypted = rc6.encrypt(plaintext, iv)
    print("Encrypted: " + str(encrypted))
    decrypted = rc6.decrypt(encrypted, iv)
    print("Decrypted: " + str(decrypted))

    app = QApplication(sys.argv)
    stylesheet = qdarkstyle.load_stylesheet_pyqt5()
    app.setStyleSheet(stylesheet)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
