from cryptography.hazmat.primitives.asymmetric import rsa, ec, padding as asymmetric_padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend

RSA_KEY_SIZE_IN_BITS = 2048
RSA_PUBLIC_EXPONENT = 65537
MASTER_PRIVATE_KEY = open(
    "/Users/surya/Desktop/Druid/c_and_c_server/MASTER_PRIVATE_KEY", "rb"
).read()


class ECC:
    def __init__(self, private_key=None, public_key=None):
        self._backend = default_backend()
        self._curve = ec.SECP256K1()

        if private_key is not None:
            self._private_key = self._load_private_key_from_byte_string(private_key)
        elif public_key is not None:
            self._public_key = self._load_public_key_from_byte_string(public_key)
        else:
            self._private_key = ec.generate_private_key(self._curve, self._backend)
            self._public_key = self._private_key.public_key()


    def _load_private_key_from_byte_string(self, private_key):
        serialized_private_key = serialization.load_pem_private_key(
            data=private_key, password=None, backend=self._backend
        )
        return serialized_private_key

    def _load_public_key_from_byte_string(self, public_key):
        serialized_public_key = serialization.load_pem_public_key(
            data=public_key, backend=self._backend
        )
        return serialized_public_key

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
