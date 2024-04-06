import socket
import threading
import sys


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except Exception as e:
            print("Error:", e)
            break


def send_messages(client_socket):
    while True:
        message = input()
        client_socket.send(message.encode('utf-8'))


def main():
    host = 'localhost'
    port = 5555

    if len(sys.argv) > 1 and sys.argv[1] == 'client':
        # if client argument is present, act as a client
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.start()

        send_thread = threading.Thread(target=send_messages, args=(client_socket,))
        send_thread.start()

        send_thread.join()
        receive_thread.join()

        client_socket.close()

    else:
        # if not, act as a server
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen()

        print("Waiting for incoming connections...")

        client_socket, client_address = server_socket.accept()
        print("Connected to: ", client_address)

        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.start()

        send_thread = threading.Thread(target=send_messages, args=(client_socket,))
        send_thread.start()

        send_thread.join()
        receive_thread.join()

        client_socket.close()
        server_socket.close()


if __name__ == "__main__":
    main()
