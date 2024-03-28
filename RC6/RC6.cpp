//
// Created by andrei-iosif on 3/15/24.
//

#include <cstring>
#include "RC6.h"

RC6::RC6(const std::vector<uint8_t>& key, uint32_t rounds, Mode mode) : rounds(rounds), key(key), mode(mode) {
    key_schedule();
}

void RC6::key_schedule() {
    // Constants gathered from RC6 Block Cipher paper - v1.1 - August 20, 1998
    uint32_t P = 0xb7e15163;
    uint32_t Q = 0x9e3779b9;
    uint32_t b = std::min(32u, (uint32_t)key.size()); // max key size is 256 bit long (32 * 8 = 256)

    uint32_t u = w / 8;

    uint32_t c = std::max(1u, b / u);
    std::vector<uint32_t> L(c);

    for(int32_t i = (int32_t)b - 1; i >= 0; --i) {
        L[i / u] = ((L[i / u] << 8) + key[i]) % modulo;
    }

    S.resize(2 * rounds + 4);
    for(uint32_t i = 0; i < 2 * rounds + 4; ++i) {
        S[i] = ((uint64_t)P + 1ULL * (uint64_t)i * Q) % modulo;
    }

    uint32_t v = 3 * std::max(c, (uint32_t)S.size());
    uint32_t A = 0, B = 0, i = 0, j = 0;

    for(uint32_t idx = 0; idx < v; ++idx) {
        A = S[i] = _lshift((S[i] + A + B) % modulo, 3);
        B = L[j] = _lshift((L[j] + A + B) % modulo, (A + B) % 32);
        i = (i + 1) % S.size();
        j = (j + 1) % c;
    }
}

uint32_t RC6::_lshift(uint32_t val, uint32_t r_bits, uint32_t max_bits) const {
    r_bits <<= max_bits - log_w;
    r_bits >>= max_bits - log_w;
    return (val << r_bits) | (val >> (w - r_bits));
}

uint32_t RC6::_rshift(uint32_t val, uint32_t r_bits, uint32_t max_bits) const {
    r_bits <<= max_bits - log_w;
    r_bits >>= max_bits - log_w;
    return (val >> r_bits) | (val << (w - r_bits));
}

std::vector<uint32_t> RC6::_encrypt_block(const std::vector<uint8_t>& plaintext) {
    std::vector<uint32_t> state(4);
    std::memcpy(&state[0], &plaintext[0], block_size);

    state[1] = (state[1] + S[0]) % modulo;
    state[3] = (state[3] + S[1]) % modulo;
    for (uint32_t i = 1; i <= rounds; ++i) {
        uint32_t t = _lshift((1ULL * state[1] * (2ULL * state[1] + 1)) % modulo, log2(w));
        uint32_t u = _lshift((1ULL * state[3] * (2ULL * state[3] + 1)) % modulo, log2(w));
        state[0] = (_lshift((state[0] ^ t), u) + S[2 * i]) % modulo;
        state[2] = (_lshift((state[2] ^ u), t) + S[2 * i + 1]) % modulo;
        std::swap(state[0], state[1]);
        std::swap(state[2], state[3]);
        std::swap(state[1], state[3]);
    }
    state[0] = (state[0] + S[2 * rounds + 2]) % modulo;
    state[2] = (state[2] + S[2 * rounds + 3]) % modulo;
    return state;
}

std::vector<uint32_t> RC6::_decrypt_block(const std::vector<uint8_t>& ciphertext) {
    std::vector<uint32_t> state(4);
    std::memcpy(&state[0], &ciphertext[0], block_size);

    state[2] = (state[2] - S[2 * rounds + 3] + modulo) % modulo;
    state[0] = (state[0] - S[2 * rounds + 2] + modulo) % modulo;
    for (uint32_t i = rounds; i > 0; --i) {
        std::swap(state[0], state[1]);
        std::swap(state[2], state[3]);
        std::swap(state[0], state[2]);
        uint32_t u = _lshift((1ULL * state[3] * (2 * state[3] + 1)) % modulo, 5);
        uint32_t t = _lshift((1ULL * state[1] * (2 * state[1] + 1)) % modulo, 5);
        state[2] = _rshift((state[2] - S[2 * i + 1] + modulo) % modulo, t) ^ u;
        state[0] = _rshift((state[0] - S[2 * i] + modulo) % modulo, u) ^ t;
    }
    state[3] = (state[3] - S[1] + modulo) % modulo;
    state[1] = (state[1] - S[0] + modulo) % modulo;
    return state;
}

std::vector<uint8_t> RC6::encrypt(const std::vector<uint8_t>& plaintext, const std::vector<uint8_t>& iv) {
    std::vector<uint8_t> encrypted;
    std::vector<uint8_t> previous_block(iv);

    if (mode == Mode::ECB) {
        // Calculate padding length
        size_t padding_length = (block_size - (plaintext.size() % block_size)) % block_size;
        // Append padding
        std::vector<uint8_t> padded_plaintext = plaintext;
        for (size_t i = 0; i < padding_length; ++i) {
            padded_plaintext.push_back(static_cast<uint8_t>(padding_length));
        }

        for (size_t i = 0; i < padded_plaintext.size(); i += block_size) {
            std::vector<uint8_t> block_to_encrypt(padded_plaintext.begin() + i, padded_plaintext.begin() + i + block_size);
            std::vector<uint32_t> encrypted_block = _encrypt_block(block_to_encrypt);
            for (uint32_t value : encrypted_block) {
                for (int j = 0; j < 4; ++j) {
                    encrypted.push_back((value >> (j * 8)) & 0xFF);
                }
            }
        }
    } else if (mode == Mode::CBC) {
        // Calculate padding length
        size_t padding_length = block_size - (plaintext.size() % block_size);
        // Append padding
        std::vector<uint8_t> padded_plaintext = plaintext;
        for (size_t i = 0; i < padding_length; ++i) {
            padded_plaintext.push_back(static_cast<uint8_t>(padding_length));
        }

        for (size_t i = 0; i < padded_plaintext.size(); i += block_size) {
            std::vector<uint8_t> block_to_encrypt(padded_plaintext.begin() + i, padded_plaintext.begin() + i + block_size);
            for (size_t j = 0; j < block_size; ++j) {
                block_to_encrypt[j] ^= previous_block[j];
            }
            std::vector<uint32_t> encrypted_block = _encrypt_block(block_to_encrypt);
            for (uint32_t value : encrypted_block) {
                for (int j = 0; j < 4; ++j) {
                    encrypted.push_back((value >> (j * 8)) & 0xFF);
                }
            }
            previous_block.assign(encrypted.end() - block_size, encrypted.end());
        }
    }

    return encrypted;
}

std::vector<uint8_t> RC6::decrypt(const std::vector<uint8_t>& ciphertext, const std::vector<uint8_t>& iv) {
    std::vector<uint8_t> decrypted;
    std::vector<uint8_t> previous_block(iv);

    if (mode == Mode::ECB) {
        for (size_t i = 0; i < ciphertext.size(); i += block_size) {
            std::vector<uint8_t> block_to_decrypt(ciphertext.begin() + i, ciphertext.begin() + i + block_size);
            std::vector<uint32_t> decrypted_block = _decrypt_block(block_to_decrypt);
            std::vector<uint8_t> temp_decrypted(block_size);
            for (size_t j = 0; j < decrypted_block.size(); ++j) {
                for (int k = 0; k < 4; ++k) {
                    temp_decrypted[j * 4 + k] = (decrypted_block[j] >> (k * 8)) & 0xFF;
                }
            }
            decrypted.insert(decrypted.end(), temp_decrypted.begin(), temp_decrypted.end());
        }
    } else if (mode == Mode::CBC) {
        for (size_t i = 0; i < ciphertext.size(); i += block_size) {
            std::vector<uint8_t> block_to_decrypt(ciphertext.begin() + i, ciphertext.begin() + i + block_size);
            std::vector<uint32_t> decrypted_block = _decrypt_block(block_to_decrypt);
            std::vector<uint8_t> temp_decrypted(block_size);
            for (size_t j = 0; j < decrypted_block.size(); ++j) {
                for (int k = 0; k < 4; ++k) {
                    temp_decrypted[j * 4 + k] = (decrypted_block[j] >> (k * 8)) & 0xFF;
                }
            }
            for (size_t j = 0; j < block_size; ++j) {
                temp_decrypted[j] ^= previous_block[j];
            }
            decrypted.insert(decrypted.end(), temp_decrypted.begin(), temp_decrypted.end());
            previous_block = block_to_decrypt;
        }
    }

    // Remove PKCS#7 padding
    size_t padding_length = decrypted.back();
    if (padding_length <= block_size) {
        decrypted.resize(decrypted.size() - padding_length);
    }

    return decrypted;
}

