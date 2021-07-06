from unittest.mock import patch

import pytest

from werkzeug.exceptions import InternalServerError, BadRequest

from signal_interpreter_server.routes import interpret_signal
from signal_interpreter_server.routes import signal_interpreter_app, parser_factory
from signal_interpreter_server.exceptions import SignalError
from signal_interpreter_server.json_parser import JsonParser


@pytest.mark.parametrize("payload, expected_status_code, expected_response", [
    ({"signal": "11"}, 200, "ECU Reset"),
    ({"dummy": "27"}, 400, None)
])
@patch.object(signal_interpreter_app, "run")
def test_interpret_signal(mock_run, payload, expected_status_code, expected_response, signal_interpreter_app_instance):
       with signal_interpreter_app_instance as client:
        with patch.object(parser_factory, "get_parser", return_value=JsonParser):
            with patch.object(JsonParser, "get_signal_title", return_value=expected_response):

                #     with tmp_app_instance as client:
                response = client.post("/", json=payload)
                if expected_response is not None:
                    tmp = {"signal_title": expected_response}
                else:
                    tmp = expected_response
                assert response.get_json() == tmp
                assert response.status_code == expected_status_code


def test_interpret_signal_with_signal_not_found(signal_interpreter_app_instance):
    with signal_interpreter_app_instance as client:
        with patch.object(parser_factory, "get_parser", return_value=JsonParser):
            with patch.object(JsonParser, "get_signal_title", side_effect=SignalError('MockedError')) as mock_get_signal:
                with pytest.raises(InternalServerError):
                    with pytest.raises(SignalError) as excinfo:
                        response = client.post("/", json={"signal": "99"})
                        assert response.get_json() is None
                        assert response.status_code == 500
                        mock_get_signal.assert_called_with("99")
                        interpret_signal()
                        assert excinfo.value.message == 'MockedError'


def test_interpret_signal_with_invalid_parser(signal_interpreter_app_instance):
    with patch.object(parser_factory, "get_parser", side_effect=ValueError('MockedError')):
        with signal_interpreter_app_instance as client:
            with pytest.raises(ValueError) as excinfo:
                response = client.post("/", json={"signal": "11"})
                assert response.get_json() is None
                assert response.status_code == 500
                assert excinfo.value.message == 'MockedError'


def test_interpret_signal_with_invalid_format(signal_interpreter_app_instance):
    with signal_interpreter_app_instance as client:
        with patch.object(parser_factory, "get_parser", return_value=JsonParser):
            with patch.object(JsonParser, "get_signal_title", side_effect=TypeError('MockedError')) as mock_get_signal:
                with pytest.raises(TypeError) as excinfo:
                    response = client.post("/", json={""})
                    assert response.get_json() is None
                    assert response.status_code == 400
                    interpret_signal()
                    assert excinfo.value.message == 'MockedError'