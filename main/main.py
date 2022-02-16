#invoked by cron periodically
import logging as log
import json

from Queries import Queries
from update_config import update_list
from searching import search, download

log.basicConfig(filename="logs/log.log", 
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                filemode="a",
                encoding='utf-8',
                level=log.INFO)

try:
    configRAW =  open("main/config.json", "r")
    config = json.load(configRAW)
    configRAW.close()
except FileNotFoundError:
    configRAW =  open("config.json", "r")
    config = json.load(configRAW)
    configRAW.close()

log.info("Scheduled Run BEGIN")
update_list(query=Queries.current_watching, userID=config["userID"], )
log.info("List Update Successfull")
res = search()
log.info("Search Successfull")
download(res)
log.info("Scheduled Run END")