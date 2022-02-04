from asyncio.subprocess import PIPE
from stat import filemode
import string
#from telnetlib import STATUS
#from tkinter import S
from bs4 import BeautifulSoup
from urllib.parse import quote
import requests
import subprocess as sb
import os
from pathlib import Path
import argparse
import logging as log
import socket
import sys

log.basicConfig(filename='xdcc.log', filemode="w", format='%(process)d-%(levelname)s-%(message)s')

def alert_my_pc(data):
    HOST, PORT = "192.168.1.66", 6666
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        log.info("Connecting to host pc")
        sock.connect((HOST, PORT))
        sock.sendall(bytes(str(data) + "\n", "utf-8"))
        log.info("Alert sent")

def getResultsPage(query):
    query = f"https://nibl.co.uk/search?query={quote(search)}"
    html = requests.get(query).text
    log.info("Gathered Results page")
    return html

def getPack(soup, bot="CR-HOLLAND|NEW"):
    selector = f'a[href="/bots/{bot}"]'
    results = soup.select(selector)
    if len(results)==0: return None
    #Traverse through the table to get the pack number 
    result = results[0].parent.parent.select("td:nth-child(2)")[0].text
    log.info("Retrieved Pack Number")
    return result

def chdir(path):
    try:
        os.chdir(path)
    except FileNotFoundError:
        os.mkdir(path)
        os.chdir(path)

def download(pack, bot="CR-HOLLAND|NEW"):
    #cmd = "[ -d \"~/home/asus/Downloads/tmp/\" ] || mkdir \"/home/asus/Downloads/tmp/\" "
    cmd = 'cd "/home/asus/Downloads/tmp/" '
    cmd += "&& "
    xdcc_command = f"xdcc -v --server irc.rizon.net --channel \"#nibl\" --nickname \"leech\" \"{bot}\" send \"{pack}\""
    xdcc_command = cmd + xdcc_command
    print(xdcc_command)
    #chdir(Path.home()+"/Downloads/_tmp/")

    process = sb.call(xdcc_command, shell=True)
    #output = process.stderr
    # if process == 0:
    #     alert_my_pc(process)
    # else:
    #     log.error("Download Failed")
    #     print("ERROR: couldn't donwload")
    #process.kill()
    
    #os.system(xdcc_command)
    
def mv():
    #[SubsPlease] Sono Bisque Doll wa Koi wo Suru - 02 (1080p) [8B775D87].mkv
    filepath = Path.home()+"/Downloads/_tmp/"




    
    
    

#search = "sono bisque 04 1080"
# botname = "CR-HOLLAND|NEW"
# bot = "/bot/"+ botname
# soup = BeautifulSoup(getResultsPage(search),"html.parser")
# pack = getPack(soup)

parser = argparse.ArgumentParser(description="xdcc automater")
parser.add_argument('-n', type=ascii, nargs=1,
                    help='Anime Name')
parser.add_argument('-ep',type=int, nargs=1,
                    help='Episode Number')
args = parser.parse_args()
#print(args.accumulate(args.integers))

name = args.n[0][1:-1]
ep = str(args.ep[0]).zfill(2)
search = f"{name} {ep} 1080"
#search = "kaginado 02 480"

soup = BeautifulSoup(getResultsPage(search),"html.parser")
pack = getPack(soup)
#download(pack)
print(pack)





