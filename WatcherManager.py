import sys
import time
import os
from threading import Lock, Thread
from selenium import webdriver
import joblib

import Watcher

TIMER = 2
# hide firefox window
os.environ['MOZ_HEADLESS'] = '1'


class WatcherManager:

    def __init__(self, watchers: dict = None):
        # watchers[chat-id] -> list of watchers
        if watchers is None:
            self.watchers = self.load_watchers()
        else:
            self.watchers: dict = watchers
        self.watchers_lock = Lock()

        self.thread = None

    def start(self):
        self.thread = Thread(target=thread_function, args=(self,))
        self.thread.start()

    def add_watcher(self, chat_id, watcher: Watcher):
        # acquire lock
        self.watchers_lock.acquire()
        try:
            if chat_id in self.watchers:
                l: list = self.watchers[chat_id]
                ok = True
                for w in l:
                    if w.name == watcher.name:
                        ok = False
                        break
                if ok:
                    l.append(watcher)
                    return True
                return False
            else:
                self.watchers[chat_id] = [watcher]
                return True
        finally:
            # release lock
            self.watchers_lock.release()

    def delete_watcher(self, chat_id, watcher_name):
        # acquire lock
        self.watchers_lock.acquire()
        try:
            if chat_id in self.watchers:
                l: list = self.watchers[chat_id]
                for watcher in l:
                    if watcher.name == watcher_name:
                        pos = l.index(watcher)
                        del l[pos]
                        return True
            return False
        finally:
            # release lock
            self.watchers_lock.release()

    def clear_watcher(self, chat_id):
        # acquire lock
        self.watchers_lock.acquire()
        try:
            if chat_id in self.watchers:
                self.watchers[chat_id].clear()
        finally:
            # release lock
            self.watchers_lock.release()

    def get_watchers(self, chat_id):
        if chat_id in self.watchers:
            return self.watchers[chat_id]
        else:
            return []

    def start_watcher(self, chat_id, watcher_name):
        # acquire lock
        self.watchers_lock.acquire()
        try:
            if chat_id in self.watchers:
                for watcher in self.watchers[chat_id]:
                    if watcher.name == watcher_name:
                        if not watcher.isRunning:
                            watcher.isRunning = True
                            return "started"
                        else:
                            return "already"
            return "not exist"
        finally:
            # release lock
            self.watchers_lock.release()

    def stop_watcher(self, chat_id, watcher_name):
        # acquire lock
        self.watchers_lock.acquire()
        try:
            if chat_id in self.watchers:
                for watcher in self.watchers[chat_id]:
                    if watcher.name == watcher_name:
                        if watcher.isRunning:
                            watcher.isRunning = False
                            return "stopped"
                        else:
                            return "already"
            return "not exist"
        finally:
            # release lock
            self.watchers_lock.release()

    def save_watchers(self):
        # acquire lock
        self.watchers_lock.acquire()
        try:
            joblib.dump(self.watchers, "watchers.pkl")
        finally:
            # release lock
            self.watchers_lock.release()

    @staticmethod
    def load_watchers():
        try:
            return joblib.load("watchers.pkl")
        except Exception as e:
            print("No watchers found on disk. Clean start")
            return {}


# routine that actually do the watcher job
def thread_function(watchers_manager: WatcherManager):
    LOG = "thread_w:"
    print(LOG, "started")
    while True:
        # acquire lock
        watchers_manager.watchers_lock.acquire()
        print(LOG, "start updating watchers")
        try:
            # start selenium browser
            browser = webdriver.Firefox()
            # for each watcher
            for user_watchers in watchers_manager.watchers.values():
                for watcher in user_watchers:
                    if watcher.isRunning:
                        browser.get(watcher.url)
                        if watcher.type == Watcher.Selector.CSS:
                            elements = browser.find_elements_by_css_selector(watcher.selector)
                            text = "".join([element.text for element in elements])
                        else:
                            text = browser.find_element_by_css_selector('body').text

                        if watcher.old_text is None:
                            watcher.old_text = text
                        else:
                            if watcher.old_text != text:
                                watcher.old_text = text
                                watcher.update.message.\
                                    reply_text("Notifier {0} has seen new changes! Go to see them:\n{1}"
                                               .format(watcher.name, watcher.url))
                                print(LOG, "updated watcher {0}".format(watcher.name))
            browser.close()
            print(LOG, "checked every running watcher")
        except Exception as e:
            print(LOG, e, file=sys.stderr)
        finally:
            # release lock
            watchers_manager.watchers_lock.release()
            # wait for next iteration
        time.sleep(TIMER)
