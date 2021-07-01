from unittest.mock import patch

import pytest

from signal_interpreter_server.routes import JsonParser
from signal_interpreter_server.main import parse_arguments, ArgumentParser
from signal_interpreter_server.main import main, signal_interpreter_app, init


class MockArgs:
    file_path = "path/to/file"


@patch.object(ArgumentParser, "add_argument")
@patch.object(ArgumentParser, "parse_args", return_value=MockArgs)
def test_parse_arguments(mock_parse_args, mock_add_argument):
    assert parse_arguments() == MockArgs
    mock_parse_args.assert_called_once()
    mock_add_argument.assert_called_with("--file_path")


@patch.object(signal_interpreter_app, "run")
@patch.object(JsonParser, "load_file")
@patch("signal_interpreter_server.main.parse_arguments", return_value=MockArgs)
def test_main(mock_parse_arguments, mock_load_file, mock_run):
    main()
    mock_parse_arguments.assert_called_once()
    mock_load_file.assert_called_with(MockArgs.file_path)
    mock_run.assert_called_once()


@patch.object(signal_interpreter_app, "run")
@patch.object(JsonParser, "load_file", side_effect=Exception('MockedError'))
@patch("signal_interpreter_server.main.parse_arguments", return_value=MockArgs)
def test_main_exception(mock_parse_arguments, mock_load_file, mock_run):
    with pytest.raises(Exception) as excinfo:
        main()
        mock_load_file.assert_called_with(MockArgs.file_path)
        assert excinfo.value.message == 'MockedError'


@patch("signal_interpreter_server.main.main")
def test_init(mock_main):
    with patch("signal_interpreter_server.main.__name__", "__main__"):
        init()
        mock_main.assert_called_once()
