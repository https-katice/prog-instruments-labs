from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import (
    load_pem_public_key,
    load_pem_private_key,
)


class Serialization:
    """
    Class for serializing and deserializing cryptographic keys
    """

    @staticmethod
    def save_symmetric_key(file_path: str, key: bytes) -> None:
        """
        Saves the symmetric key to file
        :param file_path: path to file to save
        :param key: key to save
        """
        try:
            with open(file_path, "wb") as key_file:
                key_file.write(key)
        except Exception as e:
            print("Error:", e)
            raise

    @staticmethod
    def load_symmetric_key(file_path: str) -> bytes:
        """
        Loads the symmetric key from file
        :param file_path: path to file with key
        :return: key
        """
        try:
            with open(file_path, "rb") as key_file:
                return key_file.read()
        except Exception as e:
            print("Error:", e)
            raise

    @staticmethod
    def save_private_key(path: str, private_key: rsa.RSAPrivateKey) -> None:
        """
        Saves the private RSA key to a file
        :param path: path to file to save
        :param private_key: the RSA private key
        """
        try:
            with open(path, "wb") as private_out:
                private_out.write(
                    private_key.private_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PrivateFormat.TraditionalOpenSSL,
                        encryption_algorithm=serialization.NoEncryption(),
                    )
                )
        except Exception as e:
            print("Error:", e)
            raise

    @staticmethod
    def save_public_key(path: str, public_key: rsa.RSAPublicKey) -> None:
        """
        Saves the public RSA key to a file
        :param path: path to file to save
        :param public_key: the RSA public key
        """
        try:
            with open(path, "wb") as public_out:
                public_out.write(
                    public_key.public_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PublicFormat.SubjectPublicKeyInfo,
                    )
                )
        except Exception as e:
            print("Error:", e)
            raise

    @staticmethod
    def load_private_key(path: str) -> rsa.RSAPrivateKey:
        """
        Loads a private RSA key from a file
        :param path: the path to the file that contains the key
        :return: the RSA private key
        """
        try:
            with open(path, "rb") as pem_in:
                private_bytes = pem_in.read()
                d_private_key = load_pem_private_key(
                    private_bytes,
                    password=None,
                )
            return d_private_key
        except Exception as e:
            print("Error:", e)

    @staticmethod
    def load_public_key(path: str) -> rsa.RSAPublicKey:
        """
        Loads a public RSA key from a file
        :param path: the path to the file that contains the key
        :return: the RSA public key
        """
        try:
            with open(path, "rb") as pem_in:
                public_bytes = pem_in.read()
                d_public_key = load_pem_public_key(public_bytes)
            return d_public_key
        except Exception as e:
            print("Error:", e)