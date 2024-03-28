import sys

import qdarkstyle
from PyQt5.QtWidgets import QApplication

from security import Cypher
from qtapp import MainWindow

if __name__ == '__main__':
    key = bytes.fromhex("01 23 45 67 89 ab cd ef 01 12 23 34 45 56 67 78")
    rounds = 20
    rc6 = Cypher.RC6(key, rounds, Cypher.Mode.ECB)

    plaintext = bytes.fromhex("02 13 24 35 46 57 68 79 8a 9b ac bd ce df e0 f1")
    iv = b"E49B294B0FD7A18C22EBDE4C0C8DDD56"

    encrypted = rc6.encrypt(plaintext, iv)
    print("Encrypted: " + str(encrypted.hex()))
    decrypted = rc6.decrypt(encrypted, iv)
    print("Decrypted: " + str(decrypted))

    app = QApplication(sys.argv)
    stylesheet = qdarkstyle.load_stylesheet_pyqt5()
    app.setStyleSheet(stylesheet)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
