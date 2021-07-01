import json
import logging

from signal_interpreter_server.exceptions import SignalError


logger = logging.getLogger(__name__)


class JsonParser:
    def __init__(self):
        self.data = None

    def load_file(self, file_path):
        # open the json file
        # load the json file and save it to self.data
        try:
            with open(file_path, "r") as my_file:
                self.data = json.loads(my_file.read())
            logger.info("Following signals are found in the database")
            for keys in self.data["services"]:
                signal_name_id = keys["title"] + " (" + keys["id"] + ")"
                logger.info("%s", signal_name_id)
        except (ValueError) as err:
            logger.exception(err)
            raise err

    def get_signal_title(self, identifier):
        # loop through all services in self.data
        # if the service ID is the identifier, return the title
        title = None

        for keys in self.data["services"]:
            if str(identifier) == keys["id"]:
                title = keys["title"]

        try:
            tmp = title
            tmp.swapcase()
        except AttributeError:
            logger.exception("No signal found!")
            raise SignalError

        return title
