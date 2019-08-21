from datetime import datetime

PATH_PHANTOM = open("path_phantom_js.txt").read().strip()
TIMER = 60 * 5      # seconds


def TAG():
    return str(datetime.now()) + ": "
