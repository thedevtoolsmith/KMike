from flask import Flask, request
from utils import process_request
from db import create_tables
import logging

# TODO: FIND IP AND LOCATION IN INSERT TO DB
# TODO: Implement bitcoin checks
# TODO: Check flow to return details if asked for a second time
# TODO: Check flow for unique code and key
# TODO: Find a better way to store the configuration variables

try:
    logging.basicConfig(format="%(asctime)s %(module)s %(levelname)s: %(message)s", level=logging.INFO)
    logger = logging.getLogger(__name__)
    app = Flask(__name__)
    create_tables()
except Exception as err:
    logger.error(f"Exception: {err}")



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

