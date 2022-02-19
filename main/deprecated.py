
# config = {}
# try:
#     configRAW = open("config.json", "r")
# except FileNotFoundError:
#     logger.critical("FAILED to open config.json for reading")
# config = json.load(configRAW)
# configRAW.close()

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