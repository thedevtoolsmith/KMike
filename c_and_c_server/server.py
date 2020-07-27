import logging
import random
from flask import Flask, request, json, Response
from werkzeug import exceptions
from utils import process_request
from db import create_tables


logging.basicConfig(
    format="%(asctime)s %(module)s %(levelname)s: %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
app = Flask(__name__)
create_tables()


def generate_error_message(code):
    quotes = [
        "To the well-organized mind, death is but the next great adventure.",
        "It takes a great deal of bravery to stand up to our enemies, but just as much to stand up to our friends.",
        "I'll just go down and have some pudding and wait for it all to turn up ... It always does in the end.",
        "It does not do well to dwell on dreams and forget to live.",
        "It is our choices, Harry, that show what we truly are, far more than our abilities.",
        "I solemnly swear I am up to no good.",
        "Honestly, am I the only person who's ever bothered to read 'Hogwarts: A History?'",
        "I think we've outgrown full-time education ... Time to test our talents in the real world, d'you reckon?",
        "Wit beyond measure is man’s greatest treasure.",
        "'After all this time?' 'Always,' said Snape.",
    ]
    response = Response()
    response.mimetype = "application/json"
    response.status_code = code
    if code == 418:
        response.data = "I'm a teapot"
    else:
        response.data = random.choice(quotes)
    return response


@app.route("/initialise/", methods=["POST"])
def initialise():
    return process_request(request, "initialise")


@app.route("/decrypt/", methods=["POST"])
def decrypt():
    return process_request(request, "decrypt")


@app.errorhandler(exceptions.NotFound)
def not_found(err):
    logger.error(f"Exception occured: {err}")
    return generate_error_message(404)


@app.errorhandler(exceptions.BadRequest)
def bad_request(err):
    logger.error(f"Exception occured: {err}")
    return generate_error_message(400)


@app.errorhandler(exceptions.MethodNotAllowed)
def method_not_allowed(err):
    logger.error(f"Exception occured: {err}")
    return generate_error_message(405)


@app.errorhandler(exceptions.InternalServerError)
def internal_server_error(err):
    logger.error(f"Exception occured: {err}")
    return generate_error_message(500)


@app.errorhandler(exceptions.HTTPException)
def common_error_handler(err):
    logger.error(f"Exception occured: {err}")
    return generate_error_message(418)


if __name__ == "__main__":
    app.run()

