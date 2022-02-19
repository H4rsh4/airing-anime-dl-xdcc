# invoked by cron periodically
import logging as log
import json
import sys

from Queries import Queries
from update_config import update_list
from searching import search, download

log.basicConfig(filename="logs/log.log",
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                filemode="a",
                encoding='utf-8',
                level=log.INFO)

try:
    configRAW = open("main/config.json", "r")
except FileNotFoundError:
    configRAW = open("config.json", "r")
config = json.load(configRAW)
configRAW.close()

log.info("Scheduled Run BEGIN")

config = update_list(
    config=config, query=Queries.current_watching, userID=config["userID"], )

try:
    raw = open("config.json", "w+")
except FileNotFoundError:
    log.critical("FAILED to open config.json to write data")
    sys.quit()
raw.write(json.dumps(config))
raw.close()

log.info("List Update Successfull")

res = search(config)
log.info("Search Successfull")
download(config,res)
log.info("Scheduled Run END")
