import logging.config
import os
import yaml

CURR_DIR = os.path.abspath(os.path.dirname(__file__))
LOG_FILE = os.path.join(CURR_DIR, "log_setting.yaml")

with open(LOG_FILE, "r") as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)
