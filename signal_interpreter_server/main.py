from argparse import ArgumentParser

import logging, os

from signal_interpreter_server.routes import parser_factory
from signal_interpreter_server.routes import signal_interpreter_app
from signal_interpreter_server.json_parser import JsonParser
from signal_interpreter_server.xml_parser import XmlParser



logger = logging.getLogger(__name__)


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument("--file_path")
    return parser.parse_args()


def register_parsers():
    parser_factory.register_format("JSON", JsonParser)
    parser_factory.register_format("XML", XmlParser)


def load_database(file_path):

    logger.info("Loading database from: %s", file_path)
    filename, extension = os.path.splitext(file_path)
    db_key = extension.lstrip(os.path.extsep).upper()
    parser_factory.set_signal_database_format(db_key)
    parser = parser_factory.get_parser()
    parser.load_file(file_path)


def main():

    logger.info("Server startup")
    args = parse_arguments()
    register_parsers()
    load_database(args.file_path)
    signal_interpreter_app.run()


def init():

    if __name__ == "__main__":
        main()


init()
