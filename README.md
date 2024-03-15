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

### 1.2 Implementation

#### Andrei:
- Implement RC6 cypher in C++ and bind this class to be used in Python;
- Apply some unit tests.

#### Sebastian:
- Generate vectors for testing units;
- Study RSA and create a state machine for pairing system.

_(Deadline: 22.03.2024)_

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
- Create a *.py* file to link library with the module and put this text in it.
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