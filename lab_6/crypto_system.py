from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.asymmetric import padding

from asymmetrical import AsymmetricCryptography
from serialize import Serialization
from symmetrical import SymmetricCryptography
from work_file import *


class HybridCryptoSystem:
    """
    Class implementing a hybrid crypto system using SEED (symmetric) and RSA (asymmetric) algorithms
    """

    def __init__(self, symmetric_key_path: str, private_key_path: str, public_key_path: str) -> None:
        """
        Initializes HybridCryptoSystem class object
        :param symmetric_key_path: path for saving symmetrical key
        :param private_key_path: path for saving private key
        :param public_key_path: path for saving public key
        """
        self.block_size = 128
        self.symmetric = SymmetricCryptography(symmetric_key_path)
        self.asymmetric = AsymmetricCryptography(private_key_path, public_key_path)

    def generate_keys(self, size: int) -> None:
        """
        Generates key for hybrid method
        :param size: size of keys
        """
        try:
            symmetric_key = self.symmetric.generate_key(size)
            asymmetric_key = self.asymmetric.generate_key()
            private_key, public_key = asymmetric_key

            Serialization.save_private_key(self.asymmetric.private_key_path, private_key)
            Serialization.save_public_key(self.asymmetric.public_key_path, public_key)
            write_bytes(public_key.encrypt(symmetric_key,
                                           padding.OAEP(
                                               mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                               algorithm=hashes.SHA256(),
                                               label=None,
                                           )
                                           ),
                        self.symmetric.key_path)
        except Exception as e:
            print("Error:", e)
            raise

    def encrypt(self, data_path: str, encrypted_data_path: str) -> None:
        """
        Encrypts a file using a hybrid system
        :param data_path: path to file with data
        :param encrypted_data_path: path to file for saving encrypted data
        """
        try:
            text = bytes(read_txt(data_path), "UTF-8")
            key = Serialization.load_private_key(self.asymmetric.private_key_path)
            symmetric_key = self.asymmetric.decrypt(read_bytes(self.symmetric.key_path), key)
            c_text = self.symmetric.encrypt(text, symmetric_key)
            write_bytes(c_text, encrypted_data_path)
        except Exception as e:
            print("Error:", e)
            raise

    def decrypt(self, data_path: str, decrypted_data_path: str) -> None:
        """
        Decrypts a file using a hybrid system
        :param data_path: path to file with data
        :param decrypted_data_path: path to file for saving decrypted data
        :return:
        """
        try:
            c_data = read_bytes(data_path)
            key = Serialization.load_private_key(self.asymmetric.private_key_path)
            symmetric_key = self.asymmetric.decrypt(read_bytes(self.symmetric.key_path), key)
            dc_data = self.symmetric.decrypt(c_data, symmetric_key)
            write_bytes(dc_data, decrypted_data_path)
        except Exception as e:
            print("Error:", e)
            raise