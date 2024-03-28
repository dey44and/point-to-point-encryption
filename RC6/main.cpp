#include "RC6.h"
#include <fstream>
#include <iostream>
#include <algorithm>
#include <iomanip>

using namespace std;

// Utility function to convert a hex string to a vector of uint8_t
std::vector<uint8_t> hexStringToBytes(const std::string& hex) {
    std::vector<uint8_t> bytes;

    for (size_t i = 0; i < hex.length(); i += 2) {
        uint8_t byte = std::stoi(hex.substr(i, 2), nullptr, 16);
        bytes.push_back(byte);
    }

    return bytes;
}

// Utility function to print a vector of uint8_t in hex format
void printVector(const vector<uint8_t> &hex_array, ofstream& outFile) {
    // Output the extracted values to the file
    outFile << "HEX: ";
    for (uint8_t byte : hex_array) {
        outFile << std::hex << std::setw(2) << std::setfill('0') << static_cast<int>(byte) << " ";
    }
    outFile << std::endl;
}

bool testVectors(const std::vector<uint8_t> &expected, const std::vector<uint8_t> &result) {
    // Check if the sizes of the vectors are equal
    if (expected.size() != result.size()) {
        return false;
    }

    // Iterate over each element and compare
    for (size_t i = 0; i < expected.size(); ++i) {
        if (expected[i] != result[i]) {
            return false; // Return false if any element is different
        }
    }

    // If all elements are equal, return true
    return true;
}

// Class to handle encryption and decryption tests
class TestHandler {
public:
    static void runTests(const string& inputFile, const string& outputFile) {
        ifstream fin(inputFile);
        ofstream outFile(outputFile);

        if (!fin.is_open() || !outFile.is_open()) {
            cerr << "Error opening input or output file!" << endl;
            return;
        }

        uint32_t tests;
        fin >> tests;
        fin.get(); // Consume newline after reading tests count

        // Dummy vector
        vector < uint8_t > IV = {0x0, 0x0, 0x0, 0x0};

        for (uint32_t i = 0; i < tests; ++i) {
            vector <string> data(3);
            for (uint32_t j = 0; j < 3; j++) {
                getline(fin, data[j]);
                // Remove header
                data[j] = data[j].substr(data[j].find(':') + 2, data[j].size() - 1);
                // Remove whitespaces
                data[j].erase(remove(data[j].begin(), data[j].end(), ' '), data[j].end());
            }

            std::vector<uint8_t> plaintext_bytes = hexStringToBytes(data[0]);
            std::vector<uint8_t> user_key_bytes = hexStringToBytes(data[1]);
            std::vector<uint8_t> ciphertext_bytes = hexStringToBytes(data[2]);

            RC6 cipher(user_key_bytes);
            auto result = cipher.encrypt(plaintext_bytes, IV);
            auto result_back = cipher.decrypt(result, IV);

            outFile << "Test #" << i + 1 << "\n";
            outFile << "Encryption test:\n";
            printVector(ciphertext_bytes, outFile);
            printVector(result, outFile);
            outFile << (testVectors(ciphertext_bytes, result) ? "PASSED" : "FAILED");

            outFile << "\nDecryption test:\n";
            printVector(plaintext_bytes, outFile);
            printVector(result_back, outFile);
            outFile << (testVectors(plaintext_bytes, result_back) ? "PASSED" : "FAILED");
            outFile << "\n\n";
        }

        fin.close();
        outFile.close();
    }
};

int main() {
    TestHandler::runTests("vectors.txt", "output.txt");
    return 0;
}