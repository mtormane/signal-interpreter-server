import json


class JsonParser:
    def __init__(self):
        self.data = None

    def load_file(self, file_path):
        # open the json file
        # load the json file and save it to self.data
        with open(file_path, "r") as my_file:
            fdata = my_file.read()
        self.data = json.loads(fdata)

    def get_signal_title(self, identifier):
        # loop through all services in self.data
        # if the service ID is the identifier, return the title
        for keys in self.data["services"]:
            if str(identifier) == keys["id"]:
                signal_title = keys["title"]
        return signal_title
