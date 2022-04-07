import requests
import json
import datetime, time
import logging
import re
import sys

from Queries import Queries

logger = logging.getLogger(__name__)

base_url = 'https://graphql.anilist.co'

def current_season():
    '''
    RETURNS CURRENT SEASON, YEAR
    '''
    date = datetime.date.today()
    m = date.month
    season=None
    if 3<=m<=5:
        season = "SPRING"
    elif 6<=m<=8:
        season = "SUMMER"
    elif 9<=m<=11:
        season = "FALL"
    else:
        season = "WINTER"
    return season, date.year

def process_data(raw: dict):
    '''
    This function processes the raw json data from anilist api
    return two arrays
    ids : ids of shows in user's list(maybe for future use)
    data : {Show Name : ep} that will be stored in the config.json
    '''
    SEASON, YEAR = current_season()
    ids = []
    raw = ((raw["data"]["MediaListCollection"]["lists"])[0])
    data = {}
    if raw['name'] == "Watching" and raw['status'] == 'CURRENT':
        l = raw['entries']
    else:
        return {}
    for i in l:
        #Filter: Season and year; match only anime in the current season
        if i['media']['season'] == SEASON and i['media']['seasonYear'] == YEAR:
            name = i["media"]['title']["romaji"]
            name = re.sub('[^a-zA-Z\s]', ' ', name)
            name = name.replace("  ", " ")
            #Filter: If anime HAS NOT finished airing, get current ep using the following
            if i['media']["status"] == "RELEASING":
                ep = i['media']['nextAiringEpisode']['episode'] - 1
            else:
                #If anime HAS finished, make the last ep as the current ep
                ep = i['media']['episodes']
            data[name] = ep
            ids.append(i['media']['id'])

    return ids, data


def update_list(config:dict, query: str,userID: int) -> dict:
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
    config['ids'] = ids
    config["names"] = processed
    return config


if __name__ == '__main__':
    try:
        configRAW = open("config.json", "r")
    except FileNotFoundError:
        print("FAILED to open config.json for reading")
    config = json.load(configRAW)
    configRAW.close()
    update_list(
        query=Queries.current_watching,
        userID=config["userID"],
    )
