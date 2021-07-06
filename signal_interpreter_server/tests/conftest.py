import os
import pytest


from signal_interpreter_server.json_parser import JsonParser
from signal_interpreter_server.routes import signal_interpreter_app
from signal_interpreter_server.parser_factory import ParserFactory
from signal_interpreter_server.xml_parser import XmlParser


@pytest.fixture
def signal_interpreter_app_instance():
    signal_interpreter_app.testing = True
    return signal_interpreter_app.test_client()


@pytest.fixture
def parser_factory_instance():
    return ParserFactory()


@pytest.fixture
def json_parser_instance():
    json_parser = JsonParser()
    json_parser.data = {"services": [{"title": "ECU Reset", "id": "11"}]}
    return json_parser


@pytest.fixture
def xml_parser_instance():
    xml_parser = XmlParser()
    xml_parser.data = {"services": {"service": [{"title": "ECU Reset", "@id": "11"}]}}
    return xml_parser


@pytest.fixture
def file_path():
    curr_dir = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(curr_dir, "integration", "fixtures", "test_basic.json")


@pytest.fixture
def bad_file_path():
    curr_dir = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(curr_dir, "integration", "fixtures", "fake_db.json")
