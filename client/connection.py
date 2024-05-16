import os
import socket
import threading
import time

from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import QMainWindow

from client.algebra import random_big_prime
from client.rsa import RSA
from client.security import Security


class Worker(QObject):
    update_message = pyqtSignal(str, int, str, str, str)

    def __init__(self, peer_ip: str, peer_port: int, peer_nickname: str, who_talked: str, message: str):
        self._peer_ip = peer_ip
        self._peer_port = peer_port
        self._peer_nickname = peer_nickname
        self._who_talked = who_talked
        self._message = message
        super().__init__()

    @pyqtSlot()
    def run(self):
        # Simulate some time-consuming task
        time.sleep(2)
        # Emit a signal to update the GUI with a message
        self.update_message.emit(self._peer_ip, self._peer_port, self._peer_nickname, self._who_talked, self._message)


class Peer:
    def __init__(self, name: str, ip: str, port: int, main_window: QMainWindow):
        self.__name = name
        self.__ip = ip
        self.__port = port
        self.__public_key, self.__private_key = RSA.generate_keys(128)
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__socket.bind((ip, port))
        self.__peers = {}  # Dictionary to store known peers
        self.__files = {}  # Dictionary to store current file from peer
        self.__main_window = main_window

    def __send_message(self, message: str, peer_ip: str, peer_port: int):
        # When we get a new message, check if we need to encrypt message
        if (peer_ip, peer_port) in self.__peers:
            security = self.__peers[(peer_ip, peer_port)]
            data = security.encrypt_data(message)
        else:
            data = message.encode('utf-8')
        self.__socket.sendto(data, (peer_ip, peer_port))

    def __add_peer(self, addr, peer_nick: str, peer_key: int):
        # Send a discovery message to
        security = Security(peer_key, 20)
        self.__peers[addr] = security
        peer_ip, peer_port = addr

        print(f"[INFO] Added peer {peer_nick}@{peer_ip}:{peer_port}")

        # Add item to list
        item = QStandardItem(f"{peer_nick}@{peer_ip}:{peer_port}")
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Set item as read-only
        self.__main_window.model.appendRow(item)

    def __process_request(self, command: str, body: str, addr):
        # Get command and nickname
        command_type, nickname = command.split("=")
        if command_type == 'discovery':
            # Other user wants to discover you, get data from peer
            peer_ip, peer_port = addr

            # Send back confirmation
            new_data = f"confirm_discovery={self.__name};public_key={self.__public_key}"
            self.__send_message(new_data, peer_ip, peer_port)
            print(f"[INFO] I receive a discovery message from {peer_ip}:{peer_port} and I send a confirmation message")
        elif command_type == 'confirm_discovery':
            # Add peer now and send encrypted private key
            _, public_key = body.split('=')
            peer_ip, peer_port = addr
            print(f"[INFO] I received public key: {public_key[1:-1]}")

            # If I start the connection and I receive confirmation, I should generate the secret key and encrypt
            secret_key = random_big_prime(128)

            # Generate encrypted secret key using public key from peer
            (e, N) = public_key[1:-1].split(',')
            encrypted_secret_key = RSA.encrypt((int(e), int(N)), secret_key)

            new_data = f"send_secret={self.__name};secret={encrypted_secret_key}"
            self.__send_message(new_data, peer_ip, peer_port)
            self.__add_peer(addr, nickname, secret_key)
            print(f"[INFO] I sent the secret key: {secret_key}")
        elif command_type == 'send_secret':
            # Decrypt secret from peer
            _, encrypted_secret_key = body.split('=')
            secret_key = RSA.decrypt(self.__private_key, int(encrypted_secret_key))
            self.__add_peer(addr, nickname, secret_key)
            print(f"[INFO] I received a secret key: {secret_key}")
        elif command_type == 'send_message':
            # Get message
            _, message = body.split('=')
            peer_ip, peer_port = addr

            worker = Worker(peer_ip, peer_port, nickname, nickname, message)
            worker.update_message.connect(self.__main_window.save_message)
            thread = threading.Thread(target=worker.run)
            thread.start()
        elif command_type == 'start_file':
            _, message = body.split('=')
            # Save file name
            self.__files[addr] = message
            print("\n[INFO] Start file receiving.")
        elif command_type == 'send_file':
            _, message = body.split("=", 1)
            # Get filename
            filename = self.__files[addr]
            try:
                file_path = os.path.join("../messengerApp/chat", self.__name, filename)
                with open(file_path, "ab") as file:
                    file.write(eval(message))
                print("[INFO] Received one chunk of data.")
            except IOError as e:
                print(f"[ERROR] Appending to file {filename}")
        elif command_type == 'stop_file':
            filename = self.__files[addr]
            peer_ip, peer_port = addr
            worker = Worker(peer_ip, peer_port, nickname, f"{nickname} sent file", filename)
            worker.update_message.connect(self.__main_window.save_message)
            thread = threading.Thread(target=worker.run)
            thread.start()
            # Remove file name
            del self.__files[addr]
            print("[INFO] Stop file receiving.\n")

    def discover_peer(self, peer_ip: str, peer_port: int, nickname: str):
        # Send a request for discovery
        message = f"discovery={nickname};message="
        self.__send_message(message, peer_ip, peer_port)

        print(f"[INFO] I sent a discovery message to {peer_ip}:{peer_port}")

    def send_peer_message(self, peer_ip: str, peer_port: int, message: str):
        message = f"send_message={self.__name};message={message}"
        # Send message
        self.__send_message(message, peer_ip, peer_port)

    def send_peer_file(self, peer_ip: str, peer_port: int, message_type: str, chunk):
        message = f"{message_type}={self.__name};message={chunk}"
        # Send message
        self.__send_message(message, peer_ip, peer_port)

    def listen(self):
        while True:
            data, addr = self.__socket.recvfrom(4096)
            # When we get a new message, check if we need to decrypt message
            if addr in self.__peers:
                security = self.__peers[addr]
                decoded_data = security.decrypt_data(data)
            else:
                decoded_data = data.decode('utf-8')

            command, body = decoded_data.split(";", 1)
            self.__process_request(command, body, addr)

    def start(self):
        threading.Thread(target=self.listen, daemon=True).start()
