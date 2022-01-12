from telegram.ext import Updater

from model import Selector
from config import TOKEN


class Watcher:
    name = ""
    url = ""
    type: Selector = None
    selector = None
    is_running = True
    one_shot = None
    chat_id = None
    browser_tab = None

    old_text = None

    def __init__(self, name, url, one_shot, chat_id):
        self.name = name
        self.url = url
        self.selector = None
        self.type = None
        self.is_running = True
        self.one_shot = one_shot
        self.chat_id = chat_id
        self.old_text = None
        self.browser_tab = None

    def __str__(self):
        type_str = "{0}({1})".format(self.selector, str(self.type)) if self.selector is not None else str(self.type)
        return "{0}: ({1}) {2}".format(self.name, self.url, type_str)

    def __getstate__(self):
        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()
        # Remove the unpickable entries.
        del state['browser_tab']
        return state

    def __setstate__(self, state):
        # Restore instance attributes
        self.__dict__.update(state)
        # Restore the unpickable entries
        self.browser_tab = None

    def send_message(self, message):
        updater = Updater(TOKEN)
        updater.bot.sendMessage(chat_id=self.chat_id, text=message)
