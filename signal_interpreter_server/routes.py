# routes.py
from flask import Flask, request
from signal_interpreter_server.json_parser import JsonParser

json_parser = JsonParser()

signal_interpreter_app = Flask(__name__)

@signal_interpreter_app.route("/", methods=["POST"])
def mirror_data():
    data = request.get_json()
    return data


#signal_interpreter_app.run()