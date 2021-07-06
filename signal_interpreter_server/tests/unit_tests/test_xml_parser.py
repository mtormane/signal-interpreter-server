import json
import os

from unittest.mock import patch, mock_open

from collections import OrderedDict
import pytest

from signal_interpreter_server.xml_parser import XmlParser
from signal_interpreter_server.exceptions import SignalError


# @pytest.mark.parametrize("identifier, expected_result", [
#     ("11", "ECU Reset"),
#     ("99", "Not existing"),
# ])
# def test_get_signal_title(identifier, expected_result, xml_parser_instance):
#     if identifier != '99':
#         assert xml_parser_instance.get_signal_title(identifier) == expected_result
#     else:
#         with pytest.raises(SignalError):
#             xml_parser_instance.get_signal_title(identifier)


def test_load_file_simple(xml_parser_instance):
    with patch("builtins.open",
               mock_open(read_data='<services><service id="11"><title>ECU Reset</title>'
                                   '</service></services>')):
        xml_parser_instance.load_file("path/to/xml/file")
        assert xml_parser_instance.data == {
            'services': OrderedDict([('service', OrderedDict([('@id', '11'), ('title', 'ECU Reset')]))])
        }

def test_load_file_wrong_type(xml_parser_instance):
    with patch("builtins.open", mock_open(read_data="This is wrong data!")):
        with pytest.raises(Exception):
            xml_parser_instance.load_file("path/to/xml/file")
