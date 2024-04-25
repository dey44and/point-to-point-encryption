import os
import sys

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QStandardItemModel, QTextCursor, QTextBlockFormat
from PyQt5.QtWidgets import (QMainWindow, QDialog)
from PyQt5.uic import loadUi

from client.connection import Peer
from data_dialog import DataInputDialog


def debug_trace():
    from pdb import set_trace
    QtCore.pyqtRemoveInputHook()
    set_trace()
    # QtCore.pyqtRestoreInputHook()


def extract_peer(peer_name):
    """
    Extract all relevant data from peer.
    :param peer_name: ID of the peer.
    :return: A tuple with nickname, peer_ip and peer_port.
    """
    nickname, peer_addr = peer_name.split('@')
    peer_ip, peer_port = peer_addr.split(':')
    return nickname, peer_ip, int(peer_port)


class MainWindow(QMainWindow):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    def __init__(self):
        super(MainWindow, self).__init__()
        self.__selected_item = None
        self.__socket = None
        self._name = None
        ui_path = os.path.join(self.ROOT_DIR, 'AppUI.ui')
        loadUi(ui_path, self)

        # Set a model for list view
        self.model = QStandardItemModel()
        self.listView.setModel(self.model)
        self.listView.clicked.connect(self.item_clicked)
        self.pushButton.clicked.connect(self.send_message_clicked)

        """ Initialize the fields """
        self.__peer = None
        self.config_connection()

    def item_clicked(self, index):
        """
        Called when the item from the left panel is clicked.
        :param index: Index of the item clicked.
        """
        self.__selected_item = self.model.itemFromIndex(index)
        if self.__selected_item:
            print("[INFO] Selected Item:", self.__selected_item.text())
            file_name = f"{self.__selected_item.text()}.txt"
            file_path = os.path.join("chat", self._name, file_name)
            self.update_chat(file_path)

    def send_message_clicked(self):
        """
        Called when a message is sent.
        """
        message = self.textEdit.toPlainText()
        self.textEdit.clear()
        try:
            nickname, peer_ip, peer_port = extract_peer(self.__selected_item.text())
            self.__peer.send_peer_message(peer_ip, peer_port, message)
            self.save_message(peer_ip, peer_port, nickname, self._name, message)
        except AttributeError as e:
            print(f"[ERROR] {e}")

    @pyqtSlot(str, int, str, str, str)
    def save_message(self, peer_ip: str, peer_port: int, peer_nickname: str, who_talked: str, message: str):
        """
        Save the message to the chat.
        :param peer_ip: Ip of the peer.
        :param peer_port: Port of the peer.
        :param peer_nickname: Nickname of the peer.
        :param who_talked: Nickname of who talked.
        :param message: Message to send.
        """
        print("[INFO] Save message method is triggered!")
        file_name = f"{peer_nickname}@{peer_ip}:{peer_port}.txt"
        file_path = os.path.join("chat", self._name, file_name)

        # Creating the chat directory if it doesn't exist
        if not os.path.exists(os.path.join("chat", self._name)):
            os.makedirs(os.path.join("chat", self._name))

        # Writing the message to the file
        with open(file_path, "a") as file:
            file.write(f"{who_talked}: {message}\n")
            file.close()
        self.update_chat(file_path)

    def update_chat(self, file_path):
        """
        Update the chat.
        :param file_path: Path to the file where chat is stored.
        """
        # Update chat
        self.textBrowser.clear()
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                for line in file:
                    sender, message = line.strip().split(": ", 1)
                    alignment = Qt.AlignRight if sender == self._name else Qt.AlignLeft

                    # Create a new QTextCursor at the end of the document
                    cursor = self.textBrowser.textCursor()
                    cursor.movePosition(QTextCursor.End)

                    # Insert a new block (line) into the QTextBrowser
                    cursor.insertBlock()

                    # Set the alignment for the entire block
                    block_format = QTextBlockFormat()
                    block_format.setAlignment(alignment)
                    cursor.setBlockFormat(block_format)

                    # Insert the message text
                    cursor.insertText(f"{sender}:\n{message}")
                    cursor.insertHtml("<hr style='background-color: white; height: 2px; border: 0;'>\n")

                    # Move the cursor to the end of the document
                    self.textBrowser.setTextCursor(cursor)

    def config_connection(self):
        """
        Configure the connection to the app.
        """
        dialog = DataInputDialog()
        if dialog.exec_() == QDialog.Accepted:
            # Get input values from dialog
            name = dialog.name_input.text()
            self._name = name
            self.userLabel.setText(name)
            port = int(dialog.port_input.text())

            # Further processing with the obtained values
            self.__peer = Peer(name, port, self)

            self.__peer.discover_peer('127.0.0.1', 8989, name)

            self.__peer.start()
        else:
            sys.exit(0)
