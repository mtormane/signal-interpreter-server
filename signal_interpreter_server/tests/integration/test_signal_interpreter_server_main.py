import sys
import pytest

from unittest.mock import patch

from signal_interpreter_server.main import main, signal_interpreter_app


@patch.object(signal_interpreter_app, "run")
def test_main(mock_run, file_path):
    with patch.object(sys, "argv", ["main", "--file_path", file_path]):
        signal_interpreter_app.testing = True
        tmp_app_instance = signal_interpreter_app.test_client()
        with tmp_app_instance as client:
            main()
            test_payload = {"signal": "11"}
            response = client.post("/", json=test_payload)
            assert response.get_json() == {"signal_title": "ECU Reset"}


@patch.object(signal_interpreter_app, "run")
def test_main_exception(mock_run, bad_file_path):
    with patch.object(sys, "argv", ["main", "--file_path", bad_file_path]):
        signal_interpreter_app.testing = True
        tmp_app_instance = signal_interpreter_app.test_client()
        with tmp_app_instance as client:
            with pytest.raises(TypeError):
                main()
