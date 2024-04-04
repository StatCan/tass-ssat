import logging
import logging.config
import json
from pathlib import Path

Path("./log").mkdir(parents=True, exist_ok=True)
CONFIG_PATH = "configs/log-config.json"

with open(CONFIG_PATH) as f:
    config = json.load(f)
    logging.config.dictConfig(config)

def getLogger(*name):
    logger = logging.getLogger('.'.join(['tass', *name]))
    return logger