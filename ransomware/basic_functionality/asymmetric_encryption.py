from config import RSA_PUBLIC_EXPONENT, RSA_KEY_SIZE_IN_BITS
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asymmetric_padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend


class RSA:
    def __init__(self, private_key=None, public_key=None):
        self._backend = default_backend()

        if private_key is not None:
            self._private_key = self._load_private_key_from_byte_string(private_key)
        elif public_key is not None:
            self._public_key = self._load_public_key_from_byte_string(public_key)
        else:
            self._private_key = rsa.generate_private_key(
                RSA_PUBLIC_EXPONENT, RSA_KEY_SIZE_IN_BITS, self._backend
            )
            self._public_key = self._private_key.public_key()

    def _get_padding(self):
        padder = asymmetric_padding.OAEP(
            mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        )
        return padder

    def encrypt_data(self, unencrypted_data):
        try:
            encrypted_data = self._public_key.encrypt(
                unencrypted_data, self._get_padding()
            )
        except ValueError:
            encrypted_data = self.encrypt_large_data(unencrypted_data)
        return encrypted_data

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

    def _load_public_key_from_byte_string(self, public_key):
        serialized_public_key = serialization.load_pem_public_key(
            data=public_key, backend=self._backend
        )
        return serialized_public_key

    def encrypt_large_data(self, data):
        part_size = 127
        data_in_chunks = [
            data[i : i + part_size] for i in range(0, len(data), part_size)
        ]
        encrypted_parts = [self.encrypt_data(part) for part in data_in_chunks]
        return encrypted_parts

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
