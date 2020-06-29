import hashlib
import logging
from asymmetric_encryption import RSA, ECC
from db import insert_bitcoin_details_to_database


logger = logging.getLogger(__name__)


def sha256(data):
    sha256 = hashlib.sha256()
    sha256.update(data)
    return sha256.hexdigest()


def ripemd160(data):
    ripemd160 = hashlib.new("ripemd160")
    ripemd160.update(data)
    return ripemd160.hexdigest()


def b58encode(data):
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    b58_string = ""

    leading_zeros = len(data) - len(data.lstrip("0"))
    address_int = int(data, 16)

    while address_int > 0:
        digit = address_int % 58
        digit_char = alphabet[digit]
        b58_string = digit_char + b58_string
        address_int //= 58
    ones = leading_zeros // 2
    for _ in range(ones):
        b58_string = "1" + b58_string

    return b58_string


def generate_bitcoin_wallet_id(public_key):
    logger.info("Generating Bitcoin Wallet Address from ECC Public key")
    hashed_public_key_hex = ripemd160(bytes.fromhex(sha256(public_key)))
    key_with_network_byte = f"00{hashed_public_key_hex}"
    checksum = sha256(bytes.fromhex(sha256(bytes.fromhex(key_with_network_byte))))
    address_in_hex_format = f"{key_with_network_byte}{checksum[:8]}"
    wallet_address = b58encode(address_in_hex_format)
    return wallet_address


def encode_private_key_in_wif(private_key):
    logger.info("Converting private key to WIF format")
    private_key_in_hex = private_key.hex()
    network_byte = "80"
    first_four_bytes_of_checksum = sha256(bytes.fromhex(sha256(bytes.fromhex(f"{network_byte}{private_key_in_hex}"))))[0:8]
    key_in_hex = f"{network_byte}{private_key_in_hex}{first_four_bytes_of_checksum}"
    key_in_wif = b58encode(key_in_hex)
    return key_in_wif


def generate_bitcoin_address(client_id):
    logger.info(f"Generating bitcoin payment addresses for {client_id}")
    
    cipher = ECC()
    serialized_private_key = cipher.private_key
    serialized_public_key = cipher.public_key

    wallet_address = generate_bitcoin_wallet_id(serialized_public_key)
    wif_encoded_private_key = encode_private_key_in_wif(serialized_private_key)

    insert_bitcoin_details_to_database(client_id, wallet_address, wif_encoded_private_key, serialized_public_key.decode())
    logger.info(f"Successfully inserted bitcoin details for {client_id}")

    return wallet_address


def match_bitcoin_address_and_private_key():
    return True

def verify_payment():
    return True
    
    