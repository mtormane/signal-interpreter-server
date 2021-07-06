from unittest.mock import patch

import pytest

from signal_interpreter_server.json_parser import JsonParser
from signal_interpreter_server.main import load_database, register_parsers, parser_factory
from signal_interpreter_server.main import parse_arguments, ArgumentParser
from signal_interpreter_server.main import main, signal_interpreter_app, init


class MockArgs:
    file_path = "path/to/file.ext"


@patch.object(signal_interpreter_app, "run")
def test_main(mock_run):
    with patch("signal_interpreter_server.main.parse_arguments", return_value=MockArgs) as mock_parse_arguments:
        with patch("signal_interpreter_server.main.register_parsers") as mock_register_parsers:
            with patch("signal_interpreter_server.main.load_database") as mock_load_database:
                main()
                mock_parse_arguments.assert_called_once()
                mock_register_parsers.assert_called_once()
                mock_load_database.assert_called_with("path/to/file.ext")
                mock_run.assert_called_once()


@patch.object(ArgumentParser, "add_argument")
@patch.object(ArgumentParser, "parse_args", return_value=MockArgs)
def test_parse_arguments(mock_parse_args, mock_add_argument):
    assert parse_arguments() == MockArgs
    mock_parse_args.assert_called_once()
    mock_add_argument.assert_called_with("--file_path")


def test_load_database_success():
    with patch.object(parser_factory, "set_signal_database_format") as mock_set_signal_database_format:
        with patch.object(parser_factory, "get_parser", return_value=JsonParser) as mock_get_parser:
            with patch.object(JsonParser, "load_file") as mock_load_file:
                load_database("file_path.json")
                mock_set_signal_database_format.assert_called_once()
                mock_get_parser.assert_called_once()
                mock_load_file.assert_called_with("file_path.json")


def test_load_database_exception():
    with patch.object(parser_factory, "set_signal_database_format"):
        with patch.object(parser_factory, "get_parser", return_value=JsonParser):
            with patch.object(JsonParser, "load_file", side_effect=Exception('MockedError')) as mock_load_file:
                with pytest.raises(Exception) as excinfo:
                    load_database("something")
                    mock_load_file.assert_called_with("something")
                    assert excinfo.value.message == 'MockedError'


def test_register_parsers():
    with patch.object(parser_factory, "register_format") as mock_register_parser:
        register_parsers()
        mock_register_parser.assert_called()


@patch("signal_interpreter_server.main.main")
def test_init(mock_main):
    with patch("signal_interpreter_server.main.__name__", "__main__"):
        init()
        mock_main.assert_called_once()
