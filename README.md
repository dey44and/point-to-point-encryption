# point-to-point-encryption
A distributed system of communication using encrypted messages

## 1. Objectives

### 1.1 Documentation phase

#### Andrei: 
- Study encryption proposed algorithms and create a study about pros/cons;
- Analyze possibility to write the algorithm in C++ and use CPython API to use it in a python project.

#### Sebastian:
- Study about key agreement and collect all relevant data;
- Create an interface in PyQt for the application.

_(Deadline: 08.03.2024)_

### 1.2 Implementation of RC6 algorithm

#### Andrei:
- Implement RC6 cypher in C++ and bind this class to be used in Python;
- Apply some unit tests.

#### Sebastian:
- Generate vectors for testing units;
- Study RSA and create a state machine for pairing system.

_(Deadline: 22.03.2024)_

### 1.3 Communication protocol

#### Andrei:
- Implement the logic of key agreement using Diffie-Hellman.
- Project the packets format for TCP communication.

#### Sebastian:
- Create a peer-to-peer connection using Python sockets.
- Implement binary read method for files and split them in blocks.

_(Deadline: 05.04.2024)_

## 2. Build library

- Install *pybind11* module
```bash
pip install pybind11
```
- Build RC6 project and generate *.so* file
```bash
$ cd RC6
$ g++ -c RC6.cpp -o RC6.o
$ g++ -Wall -shared -std=c++11 -fPIC $(python3 -m pybind11 --includes) RC6.o pywrap.cpp -o MyLib$(python3-config --extension-suffix)
```
- Create a *.py* file to link library with the module and put this text in it (both _.py_ and _.so_ should be moved inside same folder).
```python
def __bootstrap__():
    global __bootstrap__, __loader__, __file__
    import sys, pkg_resources, imp
    __file__ = pkg_resources.resource_filename(__name__, '[Library_File_Name].so')
    __loader__ = None;
    del __bootstrap__, __loader__
    imp.load_dynamic(__name__, __file__)


__bootstrap__()
```
- Then you can import package inside your python script and use the algorithm.
```python
from security import Cypher

if __name__ == '__main__':
    key = "a very secret password".encode("ascii")
    rounds = 16
    rc6 = Cypher.RC6(key, rounds, Cypher.Mode.ECB)

    plaintext = "This text must be encrypted".encode("ascii")
    iv = b"E49B294B0FD7A18C22EBDE4C0C8DDD56"

    encrypted = rc6.encrypt(plaintext, iv)
    decrypted = rc6.decrypt(encrypted, iv)
```

## 3. RC6 Encryption Implementation

This repository contains an implementation of the RC6 encryption algorithm in C++, along with ECB (Electronic Codebook) and CBC (Cipher Block Chaining) modes. Additionally, a Python wrapper using Pybind11 allows using the C++ implementation as a library in Python.

### 3.1 Introduction

RC6 is a symmetric key block cipher developed by Rivest et al. It is an extension of RC5, supporting variable block sizes, key sizes, and a greater number of rounds. The algorithm is efficient and secure, making it suitable for various cryptographic applications.

### 3.2 C++ Implementation

The C++ implementation of RC6 includes classes for encryption and decryption, along with support for ECB and CBC modes. The implementation follows the RC6 specification, using a specified number of rounds and key size.

### 3.3 Usage

To use the C++ implementation of RC6, include the necessary header files and link the provided library with your application. You can then create instances of the RC6 encryption/decryption classes and use them to encrypt and decrypt data.

### 3.4 Python Wrapper

The Python wrapper allows using the RC6 encryption library from Python code. Pybind11 is used to generate the Python bindings for the C++ code, enabling seamless integration between C++ and Python.

### 3.5 Example

Below is an example demonstrating how to use the RC6 encryption library from Python:

```python
from security import Cypher

# Create an instance of the RC6 encryption class
cipher = Cypher.RC6(key=b'0123456789ABCDEF', rounds=20, Cypher.Mode.CBC)
iv= b"E49B294B0FD7A18C22EBDE4C0C8DDD56"

# Encrypt data using CBC mode
encrypted_data = cipher.encrypt('Hello, RC6!'.encode('utf-8'), iv)

# Decrypt data using CBC mode
decrypted_data = cipher.decrypt(encrypted_data, iv)

print("Original:", b'Hello, RC6!')
print("Encrypted:", encrypted_data)
print("Decrypted:", decrypted_data)
```

## 4. Secret Key Exchange with RC6 and RSA

This section describes how to exchange a secret key for AES with RC6 using RSA encryption. This process ensures secure communication between a client and a server by establishing a shared AES key using asymmetric RSA encryption.

### Key Exchange Process

The key exchange process involves the following steps:

1. **Client Generates AES Key**: The client generates a random AES key to be used for symmetric encryption and decryption.

2. **Client Encrypts AES Key**: Using the server's RSA public key, the client encrypts the randomly generated AES key. This step ensures that only the server, possessing the corresponding private key, can decrypt the AES key.

3. **Client Sends Encrypted AES Key**: The client sends the encrypted AES key to the server over the network.

4. **Server Decrypts AES Key**: Upon receiving the encrypted AES key, the server decrypts it using its RSA private key. This step ensures that only the server can access the original AES key.

5. **Shared AES Key**: Both the server and the client now possess the same AES key, securely exchanged through RSA encryption. This shared key can be used for symmetric encryption and decryption using algorithms like RC6.

### Note on Server Authentication

It's essential for the client to verify the authenticity of the server to prevent man-in-the-middle attacks. Typically, this is achieved by ensuring that the server's RSA public key is authentic and belongs to the expected server. This can be done using certificates signed by trusted authorities.

### Conclusion

By exchanging a secret key for AES with RC6 using RSA encryption, the client and server can establish a shared secret key securely over an insecure network. This ensures confidentiality and integrity of the communication between the client and server.

## 5. UDP Packet Formats

This section explains the packet formats with size of 512 bytes used for UDP communication. Each packet consists of a command and associated data, formatted as `command=username;message=content`. The available command values are `discovery`, `confirm_discovery`, `send_secret`, `send_message`, `start_file`, `send_file`, and `stop_file`.

## Packet Formats

| Command           | Description         | Format                                                |
|-------------------|---------------------|-------------------------------------------------------|
| discovery         | Discovery request   | `discovery=username;message=empty`                    |
| confirm_discovery | Confirm discovery   | `confirm_discovery=username;message=peer2_public_key` |
| send_secret       | Send secret message | `send_secret=username;message=secret_key_encrypted`   |
| send_message      | Send message        | `send_message=username;message=content`               |
| start_file        | Start file transfer | `start_file=username;message=file_name`               |
| send_file         | Send file data      | `send_file=username;message=chunk`                    |
| stop_file         | Stop file transfer  | `stop_file=username;message=empty`                    |

Each packet format consists of a command field (`command`) and a message field (`message`) separated by semicolons. The `username` field represents the sender's username, and the `content` field contains the actual message or data associated with the command.
