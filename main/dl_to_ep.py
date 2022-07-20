import json
import sys
import argparse

from Queries import Queries
from update_config import update_list
from searching import search, download

import os, time, json
import logging

from xdcc_dl.pack_search import SearchEngines
from xdcc_dl.entities import XDCCPack
from xdcc_dl.xdcc import download_packs

from update_config import update_list
from Queries import Queries


try:
        configRAW = open("main/config.json", "r")
except FileNotFoundError:
    configRAW = open("config.json", "r")
config = json.load(configRAW)
configRAW.close()


def build_dir_name(seriesname: str) -> str:
    folder_name = seriesname.replace(" ", '.')
    folder_name = folder_name.strip()
    return folder_name

def change_props(xdccOBJ: XDCCPack, show):
        xdccOBJ.set_directory(config["dir"]+build_dir_name(show)+"/")
        return xdccOBJ

def check_file(config: dict, folder_name: str, filename: str, filesize: int) -> bool:
    '''
    Check if the latest aired ep is alr downloaded or not
    To avoid duplicate downloads
    '''
    folder_path = config["dir"]+folder_name
    file_path = config["dir"]+folder_name+'/'+filename
    files = []
    try:
        files = os.listdir(folder_path)
    except FileNotFoundError:
        print(f"Folder {folder_name} NOT FOUND; Creating Folder")
        os.mkdir(config["dir"]+folder_name)
        files = os.listdir(folder_path)
    if len(files) > 0 and (filename in files):
        size = os.path.getsize(file_path)
        if size >= filesize:
            return True
        else:
            print(
                f"Downloaded File smaller than New File - {filesize}>{size}")
            print(f"Deleting {filename}")
            os.remove(file_path)
    return False
def download(config, data, searches):
    '''
    Searches for each file in the folder; if it doesnt exist->download
    '''
    # searches = {series name : xdccpack}
    for name, pack in searches.items():
        if pack:
            if not check_file(config, build_dir_name(name), pack.filename, pack.size):
                print(
                    f"Downloading - {pack.filename} - {pack.packnumber} - {pack.size}")
                download_packs([pack])
            else:
                print(
                    f"File Already Exists - {pack.filename} - {pack.packnumber} - {pack.size}")
                continue




parser = argparse.ArgumentParser(description="Download all aired eps")
parser.add_argument('-n', type=ascii, nargs=1,
                    help='Anime Name')
parser.add_argument('-ep',type=int, nargs=1,
                    help='Episode Number')
args = parser.parse_args()

# show = 'Sono Bisque'
# ep = 5
#Get which episode to download until
# n
show = args.n[0][1:-1]
ep = str(args.ep[0]).zfill(2)


for ep in range(1,int(ep)+1):
    search_results = {}
    current_show_search_results = SearchEngines.NIBL.value.search(
                    show+' '+str(ep)+' '+"1080")
    for pack in current_show_search_results:
            if pack.bot == "CR-HOLLAND|NEW":
                search_results[show] = change_props(pack, show)
                break
    else:
        search_results[show] = change_props(
            current_show_search_results[0], show)
    download(config,{},search_results)
    print(search_results[show].filename)

