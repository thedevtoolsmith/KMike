import sys
import logging
import requests
import uuid
import struct
import socket
import os

logger = logging.getLogger(__name__)


def get_platform():
    """Gets the system platform

    Returns:
        str: platform
    """
    return sys.platform


def get_mac_address():
    """Get MAC address of the machine

    Returns:
        str: MAC address
    """
    return ":".join(
        hex(uuid.getnode()).strip("0x").strip("L")[i : i + 2] for i in range(0, 11, 2)
    ).upper()


def get_architecture():
    """Check if the machine has 32-bit or 64-bit architecture

    Returns:
        str: architecture
    """
    return str(int(struct.calcsize("P") * 8))


def get_device_name():
    """Get the device name

    Returns:
        str: Device name
    """
    return socket.gethostname()


def get_username():
    """Get username of the current user

    Returns:
        str: Username of the user
    """
    return os.getenv("USER", os.getenv("USERNAME", "user"))


def is_admin():
    """Checks if the user is administrator

    Returns:
        boolean: Returns True if the user is admin else false
    """
    if os.name == "nt":
        try:
            # only windows users with admin privileges can read the C:\windows\temp
            temp = os.listdir(
                os.sep.join([os.environ.get("SystemRoot", "C:\\windows"), "temp"])
            )
        except:
            return False
        else:
            return True
    else:
        if "SUDO_USER" in os.environ and os.geteuid() == 0:
            return True
        else:
            return False


def get_statistics():
    """Driver function to call other functions and collect statistics

    Returns:
        dict: A dictionary containing statistics
    """    
    stats = {
        "architecture": get_architecture,
        "platform": get_platform,
        "device_name": get_device_name,
        "mac_address": get_mac_address,
        "username": get_username,
        "is_admin": is_admin,
    }
    return {key: func() for key, func in stats.items()}

