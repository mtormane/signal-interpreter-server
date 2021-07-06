import json
import logging
import xml.etree.ElementTree as ET


import xmltodict

from signal_interpreter_server.exceptions import SignalError


logger = logging.getLogger(__name__)


class XmlParser:
    def __init__(self):
        self.data = None

    def load_file(self, file_path):
        # open the xml file
        # load the xml file and save it to self.data
        try:
            tree = ET.parse(file_path)
            data = tree.getroot()
            xml_string = ET.tostring(data, encoding="utf-8", method="xml")
            self.data = dict(xmltodict.parse(xml_string))

        except (Exception) as err:
            logger.exception(err)
            raise err


    def get_signal_title(self, identifier):
        # loop through all services in self.data
        # if the service ID is the identifier, return the title
        title = None

        for keys in self.data["service"]:
            if str(identifier) == keys["@id"]:
                title = keys["title"]

        try:
            tmp = title
            tmp.swapcase()
        except AttributeError:
            logger.exception("No signal found!")
            raise SignalError

        return title
