# routes.py
import logging

from flask import Flask, request, jsonify, abort
from werkzeug.exceptions import InternalServerError, BadRequest

from signal_interpreter_server.json_parser import JsonParser
from signal_interpreter_server.exceptions import SignalError


logger = logging.getLogger(__name__)

json_parser = JsonParser()

signal_interpreter_app = Flask(__name__)


@signal_interpreter_app.route("/", methods=["POST"])
def interpret_signal():

    try:
        data = request.get_json()
        signal_title = json_parser.get_signal_title(data["signal"])
        logger.info("Response, signal title: %s", signal_title)
    except (SignalError, InternalServerError):
        logger.exception("Signal Not Found!")
        abort(500, description=SignalError.msg)
    except (TypeError, BadRequest):
        logger.exception("Type Error!")
        abort(400, description="Input must be json object")

    return jsonify(signal_title=signal_title).get_json()
