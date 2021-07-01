from unittest.mock import patch

import pytest

from werkzeug.exceptions import InternalServerError, BadRequest

from signal_interpreter_server.routes import interpret_signal
from signal_interpreter_server.routes import signal_interpreter_app, json_parser, JsonParser
from signal_interpreter_server.exceptions import SignalError


@patch.object(json_parser, "get_signal_title", return_value="ECU Reset")
def test_interpret_signal(mock_get_signal_title):
    signal_interpreter_app.testing = True
    tmp_app_instance = signal_interpreter_app.test_client()
    with tmp_app_instance as client:
        test_payload = {"signal": "11"}
        client.post("/", json=test_payload)
        mock_get_signal_title.assert_called_with("11")
        assert interpret_signal() == {"signal_title": "ECU Reset"}


def test_interpret_signal_exception():
    signal_interpreter_app.testing = True
    tmp_app_instance = signal_interpreter_app.test_client()
    with tmp_app_instance as client:
        with pytest.raises(BadRequest):
            test_payload = "something"
            client.post("/", json=test_payload)
            interpret_signal()


@patch.object(JsonParser, "get_signal_title", side_effect=SignalError('MockedError'))
def test_interpret_signal_exception2(mock_get_signal):
    signal_interpreter_app.testing = True
    tmp_app_instance = signal_interpreter_app.test_client()
    with tmp_app_instance as client:
        with pytest.raises(InternalServerError):
            with pytest.raises(SignalError) as excinfo:
                test_payload = {"signal": "12"}
                client.post("/", json=test_payload)
                mock_get_signal.assert_called_with(test_payload["signal"])
                interpret_signal()
                assert excinfo.value.message == 'MockedError'
