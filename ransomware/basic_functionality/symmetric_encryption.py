from .config import AES_BLOCK_SIZE_IN_BITS
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend


class AES:

    def __init__(self, secret_key=None, initialization_vector=None):
            self._secret_key = secret_key
            self._initialization_vector = initialization_vector
            self._cipher = Cipher(algorithms.AES(self._secret_key),
                                  modes.CBC(self._initialization_vector),
                                  default_backend())

    def _pad_data(self, unpadded_data):
        padder = padding.PKCS7(AES_BLOCK_SIZE_IN_BITS).padder()
        padded_data = padder.update(unpadded_data) + padder.finalize()
        return padded_data

    def _unpad_data(self, padded_data):
        unpadder = padding.PKCS7(AES_BLOCK_SIZE_IN_BITS).unpadder()
        unpadded_data = unpadder.update(padded_data) + unpadder.finalize()
        return unpadded_data

    def encrypt_data(self, unencrypted_data):
        encryptor = self._cipher.encryptor()
        padded_unencrypted_data = self._pad_data(unencrypted_data)
        encrypted_data = encryptor.update(padded_unencrypted_data) + encryptor.finalize()
        return encrypted_data

    def decrypt_data(self, encrypted_data):
        decryptor = self._cipher.decryptor()
        unencrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
        unpadded_encrypted_data = self._unpad_data(unencrypted_data)
        return unpadded_encrypted_data

    @property
    def secret_key(self):
        return self._secret_key

    @secret_key.setter
    def secret_key(self, value):
        self._secret_key = value

    @property
    def initialization_vector(self):
        return self._initialization_vector

    @initialization_vector.setter
    def initialization_vector(self, value):
        self._initialization_vector = value


