import requests
import json
import time
import logging
import re
import sys

from Queries import Queries

logger = logging.getLogger(__name__)

base_url = 'https://graphql.anilist.co'

config = {}
try:
    configRAW = open("config.json", "r")
except FileNotFoundError:
    logger.critical("FAILED to open config.json for reading")
config = json.load(configRAW)
configRAW.close()


def write_to_config(ids: list, data: dict)-> list[list]:
    '''
  self-explanatory
  '''
    config['ids'] = ids
    config["names"] = data

    try:
        raw = open("config.json", "w+")
    except FileNotFoundError:
        logger.critical("FAILED to open config.json to write data")
        sys.quit()
    raw.write(json.dumps(config))
    raw.close()


def process_data(raw: dict):
    '''
    This function processes the raw json data from anilist api
    return two arrays
    ids : ids of shows in user's list(maybe for future use)
    data : {Show Name : ep} that will be stored in the config.json
    '''
    ids = []
    raw = ((raw["data"]["MediaListCollection"]["lists"])[0])
    data = {}
    if raw['name'] == "Watching" and raw['status'] == 'CURRENT':
        l = raw['entries']
    else:
        return {}
    for i in l:
        if i['media']['status'] == 'RELEASING':
            name = i["media"]['title']["romaji"]
            name = re.sub('[^a-zA-Z\s]', ' ', name)
            #name = re.sub("\s\s", "\s", name)
            name = name.replace("  ", " ")
            ep = i['media']['nextAiringEpisode']['episode'] - 1
            data[name] = ep
            ids.append(i['media']['id'])

    return ids, data


def update_list(query: str,userID: int) -> dict:
    variables = {'userId': userID}
    try:
        res = requests.post(base_url,
                            json={
                                'query': query,
                                'variables': variables
                            })
        sc = res.status_code
        if sc >= 400:
            try:
                res.raise_for_status()
            except requests.HTTPError as e:
                logging.error(e)
            return {}
    except requests.ConnectionError:
        time.sleep(300)
    ids, processed = process_data(json.loads(res.content))
    # if updateConfig:
    write_to_config(ids, processed)
    return processed


if __name__ == '__main__':

    update_list(
        query=Queries.current_watching,
        userID=config["userID"],
    )
