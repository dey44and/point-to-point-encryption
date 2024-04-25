import math
import random
from client.algebra import random_big_prime, multiplicative_inverse, fast_exp


class RSA(object):
    @staticmethod
    def generate_keys(bits_num):
        """
        Returns private and public keys of RSA.
        :param bits_num: Number of bits.
        """
        # Generate random prime numbers p and q with p != q
        p = random_big_prime(bits_num)
        q = random_big_prime(bits_num)
        while p == q:
            q = random_big_prime(bits_num)

        N = p * q
        phi = (p - 1) * (q - 1)

        # Check that e and phi are coprime
        e = random.randint(1, phi)
        g = math.gcd(e, phi)
        while g != 1:
            e = random.randint(1, phi)
            g = math.gcd(e, phi)

        # Compute the private key
        d = multiplicative_inverse(e, phi)

        return (e, N), (d, N)

    @staticmethod
    def encrypt(p_key, plaintext):
        """
        Encrypts plaintext using RSA.
        :param p_key: Public key used for encryption.
        :param plaintext: Plaintext to be encrypted.
        """
        key, n = p_key
        return fast_exp(plaintext, key, n)

    @staticmethod
    def decrypt(p_key, ciphertext):
        """
        Decrypts ciphertext using RSA.
        :param p_key: Private key used for decryption.
        :param ciphertext: Ciphertext to be decrypted.
        """
        key, n = p_key
        return fast_exp(ciphertext, key, n)
