from unittest.mock import patch
from signal_interpreter_server.routes import interpret_signal
from signal_interpreter_server.routes import signal_interpreter_app, json_parser


@patch.object(json_parser, "get_signal_title", return_value="ECU Reset")
def test_interpret_signal(mock_get_signal_title):
    signal_interpreter_app.testing = True
    tmp_app_instance = signal_interpreter_app.test_client()
    with tmp_app_instance as client:
        test_payload = {"signal": "11"}
        response = client.post("/", json=test_payload)
        mock_get_signal_title.assert_called_with("11")
        assert interpret_signal() == {"signal_title": "ECU Reset"}
        assert response.get_json() == {"signal_title": "ECU Reset"}
