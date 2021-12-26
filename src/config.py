import json

from model import Browser

file = open("../config.json", "r")
config = json.loads(file.read())
file.close()

TOKEN: str = config['token']
SELECTED_BROWSER: Browser = Browser[config['browser']]
CUSTOM_DRIVER_PATH = None
if 'custom_driver_path' in config:
    CUSTOM_DRIVER_PATH = config['custom_driver_path']
TIMER: int = int(config['timer'])
BACKUP_TIMER: str = config['backup_timer']
SAVE_PATH: str = config['save_path']
SAVE_FILE_PATH: str = SAVE_PATH + "/watchers.pkl"
