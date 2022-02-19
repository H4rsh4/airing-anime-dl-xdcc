import os,sys,re,time
import json
import logging

from xdcc_dl.pack_search import SearchEngines
from xdcc_dl.entities import XDCCPack
from xdcc_dl.xdcc import download_packs

from update_config import update_list
from Queries import Queries

"""
XDCCPack:
    server
    bot
    packnumber
    directory
    filename
    size
"""
logger = logging.getLogger(__name__)

def build_dir_name(seriesname:str) -> str:
    folder_name = seriesname.replace(" ", '.')
    folder_name = folder_name.strip()
    return folder_name

def check_file(config:dict,folder_name:str, filename:str) -> bool:
    '''
    Check if the latest aired ep is alr downloaded or not
    To avoid duplicate downloads
    '''
    files=[]
    try:
        files = os.listdir(config["dir"]+folder_name)
    except FileNotFoundError:
        logger.info(f"Folder {folder_name} NOT FOUND; Creating Folder")
        os.mkdir(config["dir"]+folder_name)
        files = os.listdir(config["dir"]+folder_name)
    if len(files)>0:
        #LATEST DOWNLOADED FILE
        latest_downloaded = files[-1]
        
        latest_downloaded_ep = re.search("[-_\s]\d\d[-_\s]", latest_downloaded)
        latest_aired_ep = re.search("[-_\s]\d\d[-_\s]", filename)
        if latest_downloaded_ep and latest_aired_ep:
            latest_downloaded_ep = latest_downloaded[latest_downloaded_ep.start():latest_downloaded_ep.end()]
            latest_downloaded_ep.strip()
            
            latest_aired_ep = filename[latest_aired_ep.start():latest_aired_ep.end()]
            latest_aired_ep.strip()

        if latest_downloaded_ep != None and int(latest_downloaded_ep)==int(latest_aired_ep):
            return True
    return False

def download(config,searches):
    '''
    Searches for each file in the folder; if it doesnt exist->download
    '''
    #searches = {series name : xdccpack}
    for name,pack in searches.items():
        if pack:
            if not check_file(config, build_dir_name(name), pack.filename):
                logger.info(f"Downloading - {pack.filename} - {pack.packnumber}")
                download_packs([pack])
            else:
                logger.info(f"File Already Exists - {pack.filename} - {pack.packnumber}")
                continue

def search(config:dict)->list:
    '''
    Searches for latest episode of each show
    only NIBL is searched
    may implement animk as well in future
    '''
    user_list = config["names"].keys()
    search_results={}

    def change_props(xdccOBJ:XDCCPack, show):
        xdccOBJ.set_directory(config["dir"]+build_dir_name(show)+"/")
        return xdccOBJ

    for show in user_list:
        ep = str(config["names"][show]).zfill(2)
        current_show_search_results = SearchEngines.NIBL.value.search(show+' '+ep+' '+str(config["resolution"]))
        #if len(current_show_search_results)==0:
        if not current_show_search_results:
            while(True):
                logger.info(f"Couldn't find latest ep of {show}\nWill Retry in 30mins")
                time.sleep(30*60)#30mins
                logger.info(f"ReSearching {show}")
                current_show_search_results = SearchEngines.NIBL.value.search(show+' '+ep+' '+str(config["resolution"]))
                if current_show_search_results: break
            
            
        #else:
        for pack in current_show_search_results:
            if pack.bot == config["preferred-bot"]:
                search_results[show] = change_props(pack, show)
                break
        else:
            search_results[show] = change_props(current_show_search_results[0], show)

    return search_results

#flow: search() -> [XDCCPacks] ==> download() ==>if not file: downloads
if __name__ == '__main__':
    
    update_list(query=Queries.current_watching, userID=config["userID"], )
    try:
        configRAW =  open("config.json", "r")
    except FileNotFoundError as e:
        print(e)
    config = json.load(configRAW)
    configRAW.close()
    res = search()
    download(res)