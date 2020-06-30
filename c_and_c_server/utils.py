from asymmetric_encryption import RSA
from base64 import b64encode, b64decode
from payment import verify_payment, generate_bitcoin_address
from db import insert_statistics_to_database
from validation import validate_decryption_request, validate_initialisation_request
import logging

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
    private_key = [
        b64decode(part) for part in request_parameters.get("private_key")
    ]
    assigned_wallet_address = b64decode(request_parameters.get("assigned_wallet_address")).decode()
    payee_wallet_address = b64decode(request_parameters.get("payee_wallet_address")).decode()
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


def the_error_message():
    return {"fun":"quote"}


def process_request(parameters, request_type):
    """Acts as a driver function to process requests

    Args:
        parameters (dict): A dict containing all the request parameters
        request_type (str): A string indicating the type of message

    Returns:
        dict: The response with various parameters included
    """    
    try:
        if request_type == "initialise" and validate_initialisation_request(parameters):
            client_id, statistics = unpack_initialise_request(parameters)
            insert_statistics_to_database(statistics, client_id)
            wallet_id = generate_bitcoin_address(client_id)
            return {"client_id": client_id, "wallet_id": wallet_id}

        elif request_type == "decrypt" and validate_decryption_request(parameters):
            client_id, private_key, assigned_wallet_address, payee_wallet_address = unpack_decrypt_request(parameters)
            if verify_payment(client_id, assigned_wallet_address, payee_wallet_address):
                return decrypt_rsa_data(private_key)
    
    except Exception as err:
        logger.error(f"Exception occured:{err}")
    
    return the_error_message()
