import json
import os
import pytest
from signal_interpreter_server.json_parser import JsonParser



jp = JsonParser()
jp.data = {"services": [{"title": "ECU Reset", "id": "11"}]}


def test_get_signal_title():
    assert jp.get_signal_title(11) == "ECU Reset"


@pytest.fixture(scope="session")
def test_load_file(tmpdir):
    tmp_db = {"services": [{"title": "ECU Reset", "id": "11"}]}
    filepath = os.path.join(tmpdir, "tmp_json.json")

    with open(filepath, 'w') as jfile:
        json.dump(tmp_db, jfile)

    jp.load_file(filepath)
    assert isinstance(jp.data, dict)
    assert jp.data == tmp_db





