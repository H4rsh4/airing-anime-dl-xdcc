
# config = {}
# try:
#     configRAW = open("config.json", "r")
# except FileNotFoundError:
#     logger.critical("FAILED to open config.json for reading")
# config = json.load(configRAW)
# configRAW.close()

# def write_to_config(ids: list, data: dict)-> list[list]:
#     '''
#   self-explanatory
#   '''
#     config['ids'] = ids
#     config["names"] = data

#     try:
#         raw = open("config.json", "w+")
#     except FileNotFoundError:
#         logger.critical("FAILED to open config.json to write data")
#         sys.quit()
#     raw.write(json.dumps(config))
#     raw.close()


# def check_file(folder_name:str, filename:str) -> bool:
#     '''
#     Check if the latest aired ep is alr downloaded or not
#     To avoid duplicate downloads
#     '''
#     files=[]
#     try:
#         files = os.listdir(config["dir"]+folder_name)
#     except FileNotFoundError:
#         logger.info(f"Folder {folder_name} NOT FOUND; Creating Folder")
#         os.mkdir(config["dir"]+folder_name)
#         files = os.listdir(config["dir"]+folder_name)
#     if len(files)>0:
#         #LATEST DOWNLOADED FILE
#         latest_downloaded = files[-1]
        
#         latest_downloaded_ep = re.search("[-_\s]\d\d[-_\s]", latest_downloaded)
#         latest_aired_ep = re.search("[-_\s]\d\d[-_\s]", filename)
#         if latest_downloaded_ep and latest_aired_ep:
#             latest_downloaded_ep = latest_downloaded[latest_downloaded_ep.start():latest_downloaded_ep.end()]
#             latest_downloaded_ep.strip()
            
#             latest_aired_ep = filename[latest_aired_ep.start():latest_aired_ep.end()]
#             latest_aired_ep.strip()

#         if latest_downloaded_ep != None and int(latest_downloaded_ep)==int(latest_aired_ep):
#             return True
#     return False