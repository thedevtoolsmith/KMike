from .encrypt_files import start_encryption
from .decrypt_files import start_decryption
import os
from .utils import generate_rsa_key_pair
from .config import LOCAL_PUBLIC_KEY


# TODO: Find a better way to store the configuration variables
# TODO: Manual Garbage Collection
# TODO: Add proper logging
# TODO: Add license and Disclaimer

# LOCAL_PUBLIC_KEY[0] = generate_rsa_key_pair()
#
# file_path = ["", ""]
# start_encryption(file_path)
# start_decryption()