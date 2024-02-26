import logging
import logging.config
import json
# TODO: load logger configs here.

CONFIG_PATH = "configs/log-config.json"

with open(CONFIG_PATH) as f:
    config = json.load(f)
    logging.config.dictConfig(config)
    print("loaded logger")

def getLogger(*name):
    logger = logging.getLogger('.'.join(['tass', *name]))
    return logger
