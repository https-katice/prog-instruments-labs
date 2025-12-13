import os

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class SymmetricCryptography:
    """
    class for symmetric encryption using the Camellia algorithm
    """
    def __init__(self, key_path: str) -> None:
        """
        initializes SymmetricCryptography class object
        :param key_path: path to key
        """
        self.key_path = key_path

    @staticmethod
    def generate_key(size: int) -> bytes:
        """
        generate key for symmetrical method
        :param size: size of key
        :return: generated key
        """
        try:
            key = os.urandom(size)
            return key
        except Exception as e:
            print("Error:", e)
            raise

    @staticmethod
    def encrypt(data: bytes, key: bytes) -> bytes:
        """
        encrypts data using the Camellia algorithm in CBC mode
        :param data: data to encrypt
        :param key: key for encryption
        :return: encrypted data in iv + ciphertext format
        """
        if len(key) not in {16, 24, 32}:
            raise ValueError("the size of key must be 16, 24, or 32 bytes")
        try:
            iv = os.urandom(16)
            cipher = Cipher(algorithms.Camellia(key), modes.CBC(iv))
            encryptor = cipher.encryptor()
            padder = padding.PKCS7(algorithms.Camellia.block_size).padder()
            padded_text = padder.update(data) + padder.finalize()
            c_text = iv + encryptor.update(padded_text) + encryptor.finalize()
            return c_text
        except Exception as e:
            print("Error:", e)
            raise

    @staticmethod
    def decrypt(data: bytes, key: bytes) -> bytes:
        """
        decrypts data encrypted with the encrypt method
        :param data: encrypted data in iv + ciphertext format
        :param key: key for decryption
        :return: decrypted data
        """
        if len(key) not in {16, 24, 32}:
            raise ValueError("the size of key must be 16, 24, or 32 bytes")
        try:
            iv = data[:16]
            data = data[16:]
            cipher = Cipher(algorithms.Camellia(key), modes.CBC(iv))
            decryptor = cipher.decryptor()
            dc_data = decryptor.update(data) + decryptor.finalize()
            unpadder = padding.PKCS7(algorithms.Camellia.block_size).unpadder()
            unpadded_dc_data = unpadder.update(dc_data) + unpadder.finalize()
            return unpadded_dc_data
        except Exception as e:
            print("Error:", e)
            raise