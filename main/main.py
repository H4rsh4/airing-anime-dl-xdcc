# invoked by cron periodically
import logging as log
import json
import sys
import argparse

from Queries import Queries
from update_config import update_list
from searching import search, download


log.basicConfig(filename="logs/log.log",
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                filemode="a",
                encoding='utf-8',
                level=log.INFO)

try:
    configRAW = open("config.json", "r")
except FileNotFoundError:
    log.critical("FAILED to open config.json to read data")
    sys.quit()
config = json.load(configRAW)
configRAW.close()

log.info("Scheduled Run BEGIN")

# config = update_list(
#     config=config, query=Queries.current_watching, userID=config["userID"], )
data = update_list(
    config=config, query=Queries.current_watching_anime, userID=config["userID"], )


try:
    raw = open("data.json", "w+")
except FileNotFoundError:
    log.critical("FAILED to open data.json to write data")
    sys.quit()
raw.write(json.dumps(data))
raw.close()

log.info("List Update Successfull")
res = search(config, data)
log.info("Search Successfull")
download(config,data, res)
log.info("Scheduled Run END")
