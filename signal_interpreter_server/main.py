from argparse import ArgumentParser

import logging

from signal_interpreter_server.routes import json_parser
from signal_interpreter_server.routes import signal_interpreter_app


logger = logging.getLogger(__name__)


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument("--file_path")
    return parser.parse_args()


def main():

    # Server startup
    logger.info("Server startup")
    args = parse_arguments()
    try:
        json_parser.load_file(args.file_path)
    except Exception as err:
        logger.exception("Database error!")
        raise err
    else:
        signal_interpreter_app.run()


def init():
    if __name__ == "__main__":
        main()


init()
