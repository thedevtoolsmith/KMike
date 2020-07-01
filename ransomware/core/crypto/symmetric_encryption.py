from . import AES_BLOCK_SIZE_IN_BITS
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend


class AES:
    def __init__(self, secret_key=None, initialization_vector=None):
        """Methods related to AES encryption, decryption and key generation

        Args:
            secret_key (bytes, optional): A random 32 byte value. Defaults to None.
            initialization_vector (bytes, optional): A random 16 byte value. Defaults to None.
        """        
        self._secret_key = secret_key
        self._initialization_vector = initialization_vector
        self._cipher = Cipher(
            algorithms.AES(self._secret_key),
            modes.CBC(self._initialization_vector),
            default_backend(),
        )


    def _pad_data(self, unpadded_data):
        """Pads the given data for encryption

        Args:
            unpadded_data (bytes): Unpadded data to be encrypted 

        Returns:
            bytes: Data with padding added
        """        
        padder = padding.PKCS7(AES_BLOCK_SIZE_IN_BITS).padder()
        padded_data = padder.update(unpadded_data) + padder.finalize()
        return padded_data


    def _unpad_data(self, padded_data):
        """Unpads the given data after decryption

        Args:
            padded_data (bytes): Decrypted data to be unpadded

        Returns:
            bytes: Data after padding is removed
        """        
        unpadder = padding.PKCS7(AES_BLOCK_SIZE_IN_BITS).unpadder()
        unpadded_data = unpadder.update(padded_data) + unpadder.finalize()
        return unpadded_data


    def encrypt_data(self, unencrypted_data):
        """Encrypts given data using AES

        Args:
            unencrypted_data (bytes): Data to be encrypted

        Returns:
            bytes: Encrypted data 
        """        
        encryptor = self._cipher.encryptor()
        padded_unencrypted_data = self._pad_data(unencrypted_data)
        encrypted_data = (
            encryptor.update(padded_unencrypted_data) + encryptor.finalize()
        )
        return encrypted_data


    def decrypt_data(self, encrypted_data):
        """Decrypt given data

        Args:
            encrypted_data (bytes): Data to be decrypted

        Returns:
            bytes: Decrypted data
        """        
        decryptor = self._cipher.decryptor()
        unencrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
        unpadded_encrypted_data = self._unpad_data(unencrypted_data)
        return unpadded_encrypted_data


    @property
    def secret_key(self):
        """Getter method for secret_key

        Returns:
            bytes: secret key of AES 
        """        
        return self._secret_key


    @secret_key.setter
    def secret_key(self, value):
        """Setter method for secret key

        Args:
            value (bytes): A random 32byte value
        """        
        self._secret_key = value


    @property
    def initialization_vector(self):
        """Getter method for initialization_vector

        Returns:
            bytes: 16 bytes AES initialization vector
        """        
        return self._initialization_vector


    @initialization_vector.setter
    def initialization_vector(self, value):
        """Setter method for initialization vector

        Args:
            value (bytes): Random 16 byte value
        """        
        self._initialization_vector = value

