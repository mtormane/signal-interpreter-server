import json


class JsonParser:
    def __init__(self):
        self.data = None

    def load_file(self, file_path):
        # open the json file
        # load the json file and save it to self.data
        with open(file_path, "r") as my_file:
            self.data = json.loads(my_file.read())

    def get_signal_title(self, identifier):
        # loop through all services in self.data
        # if the service ID is the identifier, return the title
        for keys in self.data["services"]:
            if str(identifier) == keys["id"]:
                return keys["title"]
        return None
