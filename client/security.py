from security import Cypher


class Security(object):
    """
    Security class to handle security related operations.
    """
    def __init__(self, secret_key: int, rounds: int):
        self.__secret_key = secret_key.to_bytes(128, 'big')
        self.__rounds = rounds
        self.__iv = b"E49B294B0FD7A18C22EBDE4C0C8DDD56"
        self.__rc6 = Cypher.RC6(secret_key.to_bytes(128, 'big'), 20, Cypher.Mode.CBC)

    def encrypt_data(self, message: str) -> bytes:
        """
        Encrypts message and returns encrypted message
        :param message: Message to encrypt
        """
        data = self.__rc6.encrypt(message.encode('utf-8'), self.__iv)
        return data

    def decrypt_data(self, message: bytes) -> bytes:
        """
        Decrypts message and returns decrypted message
        :param message: Message to decrypt
        """
        decoded_data = self.__rc6.decrypt(message, self.__iv).decode('utf-8')
        return decoded_data
