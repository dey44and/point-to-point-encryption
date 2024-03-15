#include <iostream>
#include <vector>
#include "RC6.h"

int main() {
    std::vector<uint8_t> key = { 't', 'h', 'i', 's', ' ', 'i', 's', ' ', 'a', ' ', 'v', 'e', 'r', 'y', ' ', 's', 'e', 'c', 'r', 'e', 't', ' ', 'k', 'e', 'y', '!', '!', '!', '!' };
    std::vector<uint8_t> iv = { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };
    RC6 rc6(key, 20);

    std::string plaintext = "Mihai, du foile alea la secretariat te rog!";
    std::vector<uint8_t> plaintext_bytes(plaintext.begin(), plaintext.end());

    std::vector<uint8_t> encrypted = rc6.encrypt(plaintext_bytes, iv);
    std::cout << "Encrypted: ";
    for (uint8_t c : encrypted) {
        printf("%02X ", c);
    }
    std::cout << std::endl;

    std::vector<uint8_t> decrypted = rc6.decrypt(encrypted, iv);
    std::cout << "Decrypted: ";
    for (uint8_t c : decrypted) {
        std::cout << c;
    }
    std::cout << std::endl;

    return 0;
}
