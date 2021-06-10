from signal_interpreter_server.main import parse_arguments, ArgumentParser, signal_interpreter_app
from signal_interpreter_server.routes import JsonParser
from unittest.mock import patch

# denna fil ska heta test_main.py
# du saknar test för main funktionen
 
class MockArgs:
    file_path = "path/to/file"

@patch.object(ArgumentParser, "add_argument")
@patch.object(ArgumentParser, "parse_args", return_value = MockArgs)
def test_parse_arguments(mock_parse_args, mock_add_argument):
    assert parse_arguments() == MockArgs
    mock_parse_args.assert_called_once()
    mock_add_argument.assert_called_with("--file_path")
    

@patch.object(signal_interpreter_app, "run")
@patch.object(JsonParser, "load_file")
@patch("signal_interpreter_server.main.parse_arguments", return_value=MockArgs)
def _test_main(mock_parse_arguments, mock_load_file, mock_run):
    main()
    mock_parse_arguments.assert_called_once()
    mock_load_file.assert_called_with(MockArgs.file_path)
    mock_run.assert_called_once()
    