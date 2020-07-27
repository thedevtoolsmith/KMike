from cryptography.hazmat.primitives.asymmetric import (
    rsa,
    ec,
    padding as asymmetric_padding,
)
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend

RSA_KEY_SIZE_IN_BITS = 2048
RSA_PUBLIC_EXPONENT = 65537
MASTER_PRIVATE_KEY = open("./MASTER_PRIVATE_KEY", "rb").read()


class ECC:
    def __init__(self, private_key=None, public_key=None):
        """Definitions related to ECC for bitcoin address generation

        Args:
            private_key (bytes, optional): ECC private key. Defaults to None.
            public_key (bytes, optional): ECC public key. Defaults to None.
        """
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
        """Loads private key from a byte string

        Args:
            private_key (bytes): ECC private key in bytestring

        Returns:
            cryptography.hazmat.primitives.asymmetric.ec.EllipticCurvePrivateKey: ECC private key object
        """
        serialized_private_key = serialization.load_pem_private_key(
            data=private_key, password=None, backend=self._backend
        )
        return serialized_private_key

    def _load_public_key_from_byte_string(self, public_key):
        """Loads public key from a byte string

        Args:
            public_key (bytes): ECC public key in bytestring

        Returns:
            cryptography.hazmat.primitives.asymmetric.ec.EllipticCurvePublicKey: ECC public key object
        """
        serialized_public_key = serialization.load_pem_public_key(
            data=public_key, backend=self._backend
        )
        return serialized_public_key

    @property
    def private_key(self):
        """Serializes an ECC private key object

        Returns:
            bytes: ECC private key as a byte string
        """
        serialized_private_key = self._private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
        return serialized_private_key

    @property
    def public_key(self):
        """Serializes an ECC public key

        Returns:
            bytes: ECC public key in bytes
        """
        serialized_public_key = self._public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        return serialized_public_key


class RSA:
    def __init__(self):
        """Uses the master key to decrypt data
        """
        self._backend = default_backend()
        self._private_key = self._load_private_key_from_byte_string(MASTER_PRIVATE_KEY)
        self._public_key = self._private_key.public_key()

    def _get_padding(self):
        """Returns padder for encryption and decryption

        Returns:
            cryptography.hazmat.primitives.asymmetric.padding.OAEP: The padder will help with padding the data to be encrypted/decrypted
        """
        padder = asymmetric_padding.OAEP(
            mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        )
        return padder

    def decrypt_data(self, encrypted_data):
        """Method to decrypt data

        Args:
            encrypted_data (bytes): Encrypted data

        Returns:
            bytes: Returns the unencrypted data
        """
        unencrypted_data = self._private_key.decrypt(
            encrypted_data, self._get_padding()
        )
        return unencrypted_data

    def _load_private_key_from_byte_string(self, private_key):
        """Loads a private key object from a byte string 

        Args:
            private_key (bytes): The RSA private key in bytes

        Returns:
            cryptography.hazmat.primitives.asymmetric.rsa.RSAPrivateKey : Private key object
        """
        serialized_private_key = serialization.load_pem_private_key(
            data=private_key, password=None, backend=self._backend
        )
        return serialized_private_key

    @property
    def private_key(self):
        """Serializes private key object

        Returns:
            bytes: Private key in bytes
        """
        serialized_private_key = self._private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
        return serialized_private_key

    @property
    def public_key(self):
        """Serializes public key object

        Returns:
            bytes: Public key in bytes
        """
        serialized_public_key = self._public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        return serialized_public_key
