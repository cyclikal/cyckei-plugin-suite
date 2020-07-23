import logging
from random import randint
from os.path import basename, join
import json

logger = logging.getLogger('cyckei')

DEFAULT_CONFIG = {
    "name":  basename(__file__)[:-3],
    "version": "0.1.dev1",
    "description": "Generates random numbers to demonstrate functionality.",
    "requirements": [],
    "sources": [
        {
            "readable": "Randomizer I",
            "port": "1",
            "range": [1, 10]
        },
        {
            "readable": "Randomizer II",
            "port": "2",
            "range": [11, 20]
        }
    ],
}


class DataController(object):
    def __init__(self, path):
        logger.info("Initializing Random Recorder plugin")

        self.name = DEFAULT_CONFIG["name"]
        with open(join(path, "plugins",
                       f"{self.name}.json")) as file:
            self.config = json.load(file)

    def match_source_attributes(self, source):
        for attr in self.config["sources"]:
            if attr["readable"] == source or attr["port"] == source:
                return attr
        logger.critical("Could not match plugin source.")
        return None

    def read(self, source):
        attr = self.match_source_attributes(source)
        if attr:
            logger.debug("Generating random integer...")
            return randint(attr["range"][0], attr["range"][1])
        return None
