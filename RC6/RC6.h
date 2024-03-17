//
// Created by andrei-iosif on 3/15/24.
//

#ifndef RC6_RC6_H
#define RC6_RC6_H

#include <cstdint>
#include <vector>
#include <valarray>

class RC6 {
public:
    enum class Mode {
        ECB,
        CBC
    };

private:
    uint32_t block_size = 16;
    uint32_t rounds;
    uint32_t w = 32;
    uint32_t log_w = (uint32_t)std::log2(w);
    int64_t modulo = (int64_t)std::pow(2, w);
    std::vector<uint32_t> S;
    std::vector<uint8_t> key;
    Mode mode; // Mode of operation

    void key_schedule();
    [[nodiscard]] uint32_t _lshift(uint32_t val, uint32_t r_bits, uint32_t max_bits = 32) const;
    [[nodiscard]] uint32_t _rshift(uint32_t val, uint32_t r_bits, uint32_t max_bits = 32) const;
    std::vector<uint32_t> _encrypt_block(const std::vector<uint8_t>& plaintext);
    std::vector<uint32_t> _decrypt_block(const std::vector<uint8_t>& ciphertext);

public:
    explicit RC6(const std::vector<uint8_t>& key, uint32_t rounds = 20, Mode mode = Mode::ECB);
    std::vector<uint8_t> encrypt(const std::vector<uint8_t>& plaintext, const std::vector<uint8_t>& iv);
    std::vector<uint8_t> decrypt(const std::vector<uint8_t>& ciphertext, const std::vector<uint8_t>& iv);
};

#endif //RC6_RC6_H
