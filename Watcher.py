import time
from enum import Enum
from multiprocessing import Process

import requests
from telegram import Update


class Selector(Enum):
    CSS = 1
    # XPATH = 2
    NONE = 3


class Watcher:
    name = ""
    url = ""
    type = None
    selector = None
    enabled = None
    update: Update = None

    thread = None
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
        self.isRunning = False

    def __str__(self):
        type_str = "{0}({1})".format(self.selector, str(self.type)) if self.selector is not None else str(self.type)
        return "{0}: ({1}) {2}".format(self.name, self.url, type_str)

    def start(self):
        try:
            self.thread = Process(target=thread_function, args=(self,))
            self.thread.start()
            self.isRunning = True
        except Exception as e:
            print(e)

    def stop(self):
        self.thread.terminate()
        self.isRunning = False


def thread_function(watcher: Watcher):
    print("thread function started for" + str(watcher))
    while True:
        try:
            html = requests.get(watcher.url).text
            soup = BeautifulSoup(html, 'html.parser')
            text = ""
            if watcher.type == Selector.CSS:
                elements = soup.select(watcher.selector)
                for elem in elements:
                    text += elem.text + "\n"
            else:
                text = soup.text

            if watcher.old_text is None:
                watcher.old_text = text
            else:
                if watcher.old_text != text:
                    watcher.old_text = text
                    watcher.update.message.reply_text("Notifier {0} has seen new changes! Go to see them:\n{1}"
                                                      .format(watcher.name, watcher.url))
            time.sleep(900)    # wait 15 minutes
        except Exception as e:
            print(e)
