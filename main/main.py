#logging pending
from distutils.command.build import build
from xdcc_dl.pack_search import SearchEngines
from xdcc_dl.xdcc import download_packs
from xdcc_dl.entities import XDCCPack

"""
XDCCPack:
    server
    bot
    packnumber
    directory
    filename
    size
"""

import os,re
import json

#from update_config import get_list,get_processed_data
from update_config import Queries, get_list

#call update_config

#Read Config
config = {}
try:
    configRAW =  open("main/config.json", "r")
    config = json.load(configRAW)
    configRAW.close()
except FileNotFoundError:
    configRAW =  open("./config.json", "r")
    config = json.load(configRAW)
    configRAW.close()
#basic test


# def chdir(path):
#     try:
#         os.chdir(path)
#     except FileNotFoundError:
#         os.mkdir(path)
#         os.chdir(path)

def build_dir_name(seriesname):
    folder_name = seriesname.replace(" ", '.')
    folder_name = folder_name.strip()
    return folder_name

def search()->list:
    series = config["names"].keys()
    search_results={}
    def process(xdccOBJ:XDCCPack, show):
        xdccOBJ.set_directory(config["dir"]+build_dir_name(show)+"/S")
        return xdccOBJ

    for show in series:
        ep = str(config["names"][show]).zfill(2)
        #print(show+' '+ep)
        tmp_search_results = SearchEngines.NIBL.value.search(show+' '+ep+' '+str(config["resolution"]))
        """
        #print(d.server)
        print(d.bot)
        print(d.packnumber)
        print(d.directory)
        d.directory = config['dir']
        print(d.directory)
        print(d.filename)
        print(d.size)
        """
        for s in tmp_search_results:
            if s.bot == config["preferred-bot"]:
                #s = process(s)
                search_results[show] = process(s, show)
                break
        else:
            #process(tmp_search_results[0])
            search_results[show] = process(tmp_search_results[0], show)

    return search_results

def check_file(folder_name, filename):
    # folder_name = seriesname.replace(" ", '.')
    # folder_name = folder_name.strip()
    #folder_name = seriesname
    #mkdir if not folder exists
    files=[]
    try:
        files = os.listdir(config["dir"]+folder_name)
    except FileNotFoundError:
        os.mkdir(config["dir"]+folder_name)
        files = os.listdir(config["dir"]+folder_name)
    #print(files)
    if len(files)>0:
        #LATEST DOWNLOADED FILE
        latest = files[-1]
        
        latest_ep = re.search("[-_\s]\d\d[-_\s]", latest)
        ep = re.search("[-_\s]\d\d[-_\s]", filename)
        if latest_ep and ep:
            latest_ep = latest[latest_ep.start():latest_ep.end()]
            latest_ep.strip()
            #LATEST AIRED EP
            
            ep = filename[ep.start():ep.end()]
            ep.strip()

        #print(ep)
        if latest_ep != None and int(latest_ep)==int(ep):
            return True
    return False

def download(searches):
    '''
    Searches for each file in the folder; it it doesnt exist->download
    '''
    #{series name : xdccpack}
    #print(searches)
    for name,pack in searches.items():
        #checkfile(name, pack.filename)
        if pack:
            if not check_file(build_dir_name(name), pack.filename):
                print("DOWNLOAD")
                download_packs([pack])
            else:
                print("files exists")
                #log file exists
                continue


#flow: search() -> [XDCCPacks] ==> download() ==>if not file: downloads
if __name__ == '__main__':
    
    get_list(query=Queries.current_watching, userID=config["userID"], )
    try:
        configRAW =  open("main/config.json", "r")
        config = json.load(configRAW)
        configRAW.close()
    except FileNotFoundError:
        configRAW =  open("config.json", "r")
        config = json.load(configRAW)
        configRAW.close()
    res = search()
    download(res)