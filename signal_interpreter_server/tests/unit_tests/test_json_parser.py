import json
import os

from unittest.mock import patch, mock_open

import pytest

from signal_interpreter_server.json_parser import JsonParser
from signal_interpreter_server.exceptions import SignalError


@pytest.mark.parametrize("identifier, expected_result", [
    ("11", "ECU Reset"),
    ("99", "Not existing"),
])
def test_get_signal_title(identifier, expected_result):
    jason_parser = JsonParser()
    jason_parser.data = {"services": [{"title": "ECU Reset", "id": "11"}]}
    if identifier != '99':
        assert jason_parser.get_signal_title(identifier) == expected_result
    else:
        with pytest.raises(SignalError):
            jason_parser.get_signal_title(identifier)


@pytest.fixture(scope="session")
def test_load_file_with_fixure(tmpdir):
    tmp_db = {"services": [{"title": "ECU Reset", "id": "11"}]}
    filepath = os.path.join(tmpdir, "tmp_json.json")

    with open(filepath, 'w') as jfile:
        json.dump(tmp_db, jfile)
    jason_parser = JsonParser()
    jason_parser.load_file(filepath)
    assert isinstance(jason_parser.data, dict)
    assert jason_parser.data == tmp_db


def test_load_file_simple():
    with patch("builtins.open",
               mock_open(read_data='{"services": [{"title": "ECU Reset", "id": "11"}]}')):
        json_parser = JsonParser()
        json_parser.load_file("path/to/json/file")
        assert json_parser.data == {"services": [{"title": "ECU Reset", "id": "11"}]}


def test_load_file_wrong_type():
    with patch("builtins.open", mock_open(read_data="This is wrong data!")):
        with pytest.raises(ValueError):
            json_parser = JsonParser()
            json_parser.load_file("path/to/json/file")
