from signal_interpreter_server.routes import signal_interpreter_app
from argparse import ArgumentParser
from signal_interpreter_server.routes import json_parser
from signal_interpreter_server.json_parser import JsonParser

def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument("--file_path")
    return parser.parse_args()

def main():

    #Server startup
    args = parse_arguments()
    json_parser.load_file(args.file_path)
    signal_interpreter_app.run()

if __name__ == "__main__":
    main()

