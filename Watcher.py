from enum import Enum
from multiprocessing import Process

from telegram import Update


class Selector(Enum):
    CSS = 1
    XPATH = 2
    NONE = 3


class Watcher:
    name: str
    url: str
    type: Selector
    selector: str
    enabled: bool
    update: Update

    thread: Process

    def __init__(self, name, url, update):
        self.name = name
        self.url = url
        self.selector = None
        self.type = None
        self.enabled = True
        self.update = update

        self.thread = Process(target=thread_function, args=(self,))

    def __str__(self):
        type_str = "{0}({1})".format(self.selector, str(self.type)) if self.selector is not None else str(self.type)
        return "{0}: ({1}) {2}".format(self.name, self.url, type_str)

    def start(self):
        self.thread.start()

    def stop(self):
        self.thread.terminate()


def thread_function(watcher: Watcher):
    pass