#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "RC6.h"

namespace py = pybind11;
constexpr auto byref = py::return_value_policy::reference_internal;

PYBIND11_MODULE(Cypher, m) {
    m.doc() = "Pybind11 plugin for RC6 encryption and decryption";

    py::enum_<RC6::Mode>(m, "Mode")
            .value("ECB", RC6::Mode::ECB)
            .value("CBC", RC6::Mode::CBC)
            .export_values();

    py::class_<RC6>(m, "RC6")
            .def(py::init([](const py::bytes& key, uint32_t rounds, RC6::Mode mode) {
                std::string keyStr = key; // Implicit conversion from py::bytes to std::string
                std::vector<uint8_t> keyVec(keyStr.begin(), keyStr.end());
                return new RC6(keyVec, rounds, mode);
            }))
            .def("encrypt", [](RC6& self, const py::bytes& plaintext, const py::bytes& iv) {
                std::string plaintextStr = plaintext; // Convert py::bytes to std::string
                std::string ivStr = iv; // Convert py::bytes to std::string
                std::vector<uint8_t> plaintextVec(plaintextStr.begin(), plaintextStr.end());
                std::vector<uint8_t> ivVec(ivStr.begin(), ivStr.end());

                auto encryptedVec = self.encrypt(plaintextVec, ivVec);

                // Convert std::vector<uint8_t> back to py::bytes
                return py::bytes(std::string(encryptedVec.begin(), encryptedVec.end()));
            }, py::call_guard<py::gil_scoped_release>(), py::arg("plaintext"), py::arg("iv"))
            .def("decrypt", [](RC6& self, const py::bytes& ciphertext, const py::bytes& iv) {
                std::string ciphertextStr = ciphertext; // Convert py::bytes to std::string
                std::string ivStr = iv; // Convert py::bytes to std::string
                std::vector<uint8_t> ciphertextVec(ciphertextStr.begin(), ciphertextStr.end());
                std::vector<uint8_t> ivVec(ivStr.begin(), ivStr.end());

                auto decryptedVec = self.decrypt(ciphertextVec, ivVec);

                // Convert std::vector<uint8_t> back to py::bytes
                return py::bytes(std::string(decryptedVec.begin(), decryptedVec.end()));
            }, py::call_guard<py::gil_scoped_release>(), py::arg("ciphertext"), py::arg("iv"));
}
