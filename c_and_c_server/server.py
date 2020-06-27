from flask import Flask, request
from base64 import b64decode, b64encode
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asymmetric_padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
import logging

logging.basicConfig(
    format="%(asctime)s %(module)s %(levelname)s: %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

RSA_KEY_SIZE_IN_BITS = 2048
RSA_PUBLIC_EXPONENT = 65537
MASTER_PRIVATE_KEY = open(
    "/Users/surya/Desktop/Druid/c_and_c_server/MASTER_PRIVATE_KEY", "rb"
).read()


class RSA:
    def __init__(self):
        self._backend = default_backend()
        self._private_key = self._load_private_key_from_byte_string(MASTER_PRIVATE_KEY)
        self._public_key = self._private_key.public_key()

    def _get_padding(self):

        padder = asymmetric_padding.OAEP(
            mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        )
        return padder

    def decrypt_data(self, encrypted_data):
        unencrypted_data = self._private_key.decrypt(
            encrypted_data, self._get_padding()
        )
        return unencrypted_data

    def _load_private_key_from_byte_string(self, private_key):
        serialized_private_key = serialization.load_pem_private_key(
            data=private_key, password=None, backend=self._backend
        )
        return serialized_private_key

    @property
    def private_key(self):
        serialized_private_key = self._private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
        return serialized_private_key

    @property
    def public_key(self):
        serialized_public_key = self._public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        return serialized_public_key


def decrypt_rsa_key(encrypted_key):
    logger.info("Decrypting RSA key")
    cipher = RSA()
    unencrypted_local_private_key = b"".join(
        [cipher.decrypt_data(key_part) for key_part in encrypted_key]
    )
    payload = {"key": b64encode(unencrypted_local_private_key).decode("ascii")}
    return payload


@app.route("/decrypt", methods=["POST"])
def hello_world():
    request_data = request.get_json()
    if request_data.get("payload"):
        return decrypt_rsa_key(
            [b64decode(part) for part in request_data.get("payload")]
        )
    else:
        return {
            "message": "He killed three men in a bar with a pencil, WITH A F'KIN PENCIL"
        }


if __name__ == "__main__":
    app.run()

