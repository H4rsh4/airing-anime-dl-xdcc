#logging pending
import requests
import json
import time
import logging as log
import re
from Queries import Queries

log.basicConfig(filename="api.log", 
                format="%(asctime)s %(message)s",
                filemode="w",
                encoding='utf-8')

base_url  = 'https://graphql.anilist.co'

config = {}
try:
    configRAW =  open("main/config.json", "r")
    config = json.load(configRAW)
    configRAW.close()
except FileNotFoundError:
    configRAW =  open("./config.json", "r")
    config = json.load(configRAW)
    configRAW.close()

def write_to_config(ids:list,data:dict):
  # raw = open("config.json", "r")
  # current = json.load(raw)
  # raw.close()

  config['ids'] = ids
  config["names"] = data

  raw = open("main/config.json", "w+")
  raw.write(json.dumps(config))
  raw.close()

def get_processed_data(raw:dict):
    ids=[]
    raw = ((raw["data"]["MediaListCollection"]["lists"])[0])
    final = {}
    if raw['name']=="Watching" and raw['status']=='CURRENT':
        l = raw['entries']
    else:
        return {}
    for i in l:
        if i['media']['status'] =='RELEASING':
            name = i["media"]['title']["romaji"]
            name = re.sub('[^a-zA-Z\s]', ' ', name)
            #name = re.sub("\s\s", "\s", name)
            name = name.replace("  ", " ")
            ep = i['media']['nextAiringEpisode']['episode']-1
            final[name] = ep
            ids.append(i['media']['id'])

    return ids,final

def get_list(query:str, userID:int,)-> dict:
    variables={
        'userId' : userID
    }
    try:
        res = requests.post(base_url, json={'query':query, 'variables':variables})
        sc = res.status_code
        if sc >= 400:
            try:
                res.raise_for_status()
            except requests.HTTPError as e:
                log.error(e)
            return{}
    except requests.ConnectionError:
        time.sleep(300)
    ids,processed = get_processed_data(json.loads(res.content))
    #if updateConfig: 
    write_to_config(ids,processed)
    return processed

if __name__ == '__main__':

  get_list(query=Queries.current_watching, userID=config["userID"], )
















