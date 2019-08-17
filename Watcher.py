from enum import Enum

from telegram import Update


class Selector(Enum):
    CSS = 1
    NONE = 2


class Watcher:
    name = ""
    url = ""
    type = None
    selector = None
    enabled = None
    update: Update = None

    old_text = None
    isRunning = None

    def __init__(self, name, url, update):
        self.name = name
        self.url = url
        self.selector = None
        self.type = None
        self.enabled = True
        self.update = update
        self.old_text = None
        self.isRunning = True

    def __str__(self):
        type_str = "{0}({1})".format(self.selector, str(self.type)) if self.selector is not None else str(self.type)
        return "{0}: ({1}) {2}".format(self.name, self.url, type_str)



