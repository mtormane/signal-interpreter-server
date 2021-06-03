from unittest.mock import patch,mock_open
from signal_interpreter_server.json_parser import JsonParser

jp = JsonParser()
jp.data={"services": [{"title": "ECU Reset", "id": "11"}]}

def test_get_signal_title():
    assert jp.get_signal_title(11) == "ECU Reset"

def test_load_file():
    jp.load_file("C:\data\python\course\my_project\signal-interpreter-server\signal_database.json")
    assert isinstance(jp.data, dict)
