from core.crypto.asymmetric_encryption import RSA
from core.config import (
    MASTER_PUBLIC_KEY,
    ENCRYPTED_LOCAL_RSA_PRIVATE_KEY_FILE_LOCATION,
    CLIENT_ID_LOCATION,
    LOCAL_RSA_PUBLIC_KEY_FILE_LOCATION
)
from core.utils.file_ops import write_data_to_file, read_data_from_file
import logging
import os
import uuid

logger = logging.getLogger()


def generate_rsa_key_pair():
    """Generates new RSA key pair and encrypts the private key before storing it on disk

    Returns:
        bytes: Serialized RSA public key
    """
    logger.info("Generating RSA key pair")
    cipher = RSA()
    serialized_private_key = cipher.private_key
    serialized_public_key = cipher.public_key

    logger.info("Encrypting RSA private key")
    cipher = RSA(public_key=MASTER_PUBLIC_KEY)
    encrypted_private_key = cipher.encrypt_large_data(serialized_private_key)

    logger.info("Storing encrypted RSA private key in disk")
    write_data_to_file(
        ENCRYPTED_LOCAL_RSA_PRIVATE_KEY_FILE_LOCATION, encrypted_private_key, False
    )

    write_data_to_file(
        LOCAL_RSA_PUBLIC_KEY_FILE_LOCATION, serialized_public_key, False
    )

    return serialized_public_key


def generate_client_id():
    """Generates a random client ID

    Returns:
        str: The client ID in UUID4 format
    """
    if os.path.exists(CLIENT_ID_LOCATION):
        client_id = read_data_from_file(CLIENT_ID_LOCATION).decode()
    else:
        client_id = str(uuid.uuid4())
        write_data_to_file(CLIENT_ID_LOCATION, client_id.encode())
    return client_id
