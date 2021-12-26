import json

from src import model

file = open("../config.json", "r")
config = json.loads(file.read())
file.close()

TOKEN: str = config['token']
SELECTED_BROWSER: model = config['browser']
TIMER: int = int(config['timer'])
SAVE_PATH: str = config['save_path']
SAVE_FILE_PATH: str = SAVE_PATH + "/watchers.pkl"


