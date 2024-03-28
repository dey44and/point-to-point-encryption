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