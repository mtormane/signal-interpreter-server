# routes.py
import logging

from flask import Flask, request, jsonify, abort
from werkzeug.exceptions import InternalServerError, BadRequest

from signal_interpreter_server.parser_factory import ParserFactory
from signal_interpreter_server.exceptions import SignalError


logger = logging.getLogger(__name__)

parser_factory = ParserFactory()


signal_interpreter_app = Flask(__name__)


@signal_interpreter_app.route("/", methods=["POST"])
def interpret_signal():

    try:
        data = request.get_json()
        signal_title = parser_factory.get_parser().get_signal_title(data["signal"])
        logger.info("Response, signal title: %s", signal_title)
    except (SignalError, InternalServerError):
        logger.exception("Signal Not Found!")
        abort(500, description=SignalError.msg)
    except (TypeError):
        logger.exception("Type Error!")
        abort(400, description="Input must be json object")
    except KeyError:
        logger.exception("Key Error!")
        abort(400, description="Key not found in dict")

    return jsonify(signal_title=signal_title).get_json()
