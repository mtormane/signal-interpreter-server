from signal_interpreter_server.json_parser import JsonParser
import json, os, pytest

jp = JsonParser()
jp.data={"services": [{"title": "ECU Reset", "id": "11"}]}

def test_get_signal_title():
    assert jp.get_signal_title(11) == "ECU Reset"

@pytest.fixture(scope="session")
def test_load_file(tmpdir):
    tmp_db = {"services": [{"title": "ECU Reset", "id": "11"}]}
    filepath = os.path.join(tmpdir,"tmp_json.json")

    # vi kan mocka bort open, se lösningsförslag. Går även med dekorator.
    # Vi tittar närmare på fixture i lektion 4
    with open(filepath, 'w') as jfile:
        json.dump(tmp_db, jfile)

    jp.load_file(filepath)
    assert isinstance(jp.data, dict)
    assert jp.data == tmp_db
