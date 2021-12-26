import os
import sys
import time
from threading import Lock, Thread

import joblib
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.opera import OperaDriverManager
from webdriver_manager.utils import ChromeType

import Watcher
from config import SELECTED_BROWSER, SAVE_PATH, SAVE_FILE_PATH, TIMER
from model import Browser, Selector
from utils import print_tag, flush

watchers_lock = Lock()


class WatcherManager:

    def __init__(self, watchers: dict = None):
        # watchers[chat-id] -> list of watchers
        if watchers is None:
            self.watchers = self.load_watchers()
        else:
            self.watchers: dict = watchers
        self.thread = None

    def start(self):
        self.thread = Thread(target=thread_function, args=(self,))
        self.thread.start()

    def add_watcher(self, chat_id, watcher: Watcher):
        # acquire lock
        watchers_lock.acquire()
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
                    open_tab(watcher)
                    watcher.old_text = get_value_from_watcher_selector(watcher)
                    return True
                return False
            else:
                self.watchers[chat_id] = [watcher]
                return True
        finally:
            # release lock
            watchers_lock.release()

    def delete_watcher(self, chat_id, watcher_name):
        # acquire lock
        watchers_lock.acquire()
        try:
            if chat_id in self.watchers:
                l: list = self.watchers[chat_id]
                for watcher in l:
                    if watcher.name == watcher_name:
                        pos = l.index(watcher)
                        close_tab(watcher)
                        del l[pos]
                        return True
            return False
        finally:
            # release lock
            watchers_lock.release()

    def clear_watcher(self, chat_id):
        # acquire lock
        watchers_lock.acquire()
        try:
            if chat_id in self.watchers:
                self.watchers[chat_id].clear()
        finally:
            # release lock
            watchers_lock.release()

    def get_watchers(self, chat_id):
        if chat_id in self.watchers:
            return self.watchers[chat_id]
        else:
            return []

    def start_watcher(self, chat_id, watcher_name):
        # acquire lock
        watchers_lock.acquire()
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
            watchers_lock.release()

    def stop_watcher(self, chat_id, watcher_name):
        # acquire lock
        watchers_lock.acquire()
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
            watchers_lock.release()

    def save_watchers(self):
        # acquire lock
        if not os.path.isdir(SAVE_PATH):
            os.makedirs(SAVE_PATH)
        watchers_lock.acquire()
        try:
            joblib.dump(self.watchers, SAVE_FILE_PATH)
        finally:
            # release lock
            watchers_lock.release()

    @staticmethod
    def load_watchers():
        try:
            return joblib.load(SAVE_FILE_PATH)
        except Exception as e:
            print("No watchers found on disk. Clean start")
            return {}


def get_webdriver(selected: Browser) -> webdriver:
    if selected == Browser.FIREFOX:
        return webdriver.Firefox(executable_path=GeckoDriverManager().install())
    elif selected == Browser.CHROME:
        return webdriver.Chrome(ChromeDriverManager().install())
    elif selected == Browser.CHROMIUM:
        return webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
    elif selected == Browser.EDGE:
        return webdriver.Edge(EdgeChromiumDriverManager().install())
    elif selected == Browser.OPERA:
        return webdriver.Opera(executable_path=OperaDriverManager().install())
    else:
        return None


def open_tab(watcher: Watcher):
    browser.switch_to.new_window('tab')
    browser.get(watcher.url)
    tab = browser.window_handles[-1]
    browser.switch_to.window(tab)
    return tab


def close_tab(watcher: Watcher):
    if watcher.browser_tab is not None:
        browser.switch_to.window(watcher.browser_tab)
        browser.close()


def get_value_from_watcher_selector(watcher: Watcher):
    if watcher.type == Selector.CSS:
        elements = browser.find_elements(By.CSS_SELECTOR, watcher.selector)
        return "".join([element.text for element in elements])
    elif watcher.type == Selector.NONE:
        return browser.find_element(By.TAG_NAME, 'body').text
    else:
        return ""


# start browser
browser = get_webdriver(SELECTED_BROWSER)


# routine that actually do the watcher job
def thread_function(watchers_manager: WatcherManager):
    LOG = "thread_watchers:"
    print_tag(LOG, "started")
    while True:
        # acquire lock
        watchers_lock.acquire()
        print_tag(LOG, "start updating watchers")
        # for each watcher
        for user_watchers in watchers_manager.watchers.values():
            for watcher in user_watchers:
                try:
                    if watcher.enabled:
                        if watcher.browser_tab is None:
                            watcher.browser_tab = open_tab(watcher)
                        else:
                            browser.switch_to.window(watcher.browser_tab)
                            browser.refresh()
                        text: str = get_value_from_watcher_selector(watcher)
                        if watcher.old_text is None:
                            watcher.old_text = text
                        else:
                            if watcher.old_text != text:
                                watcher.old_text = text
                                message: str = "Notifier {0} has seen new changes! Go to see them:\n{1}".format(
                                    watcher.name, watcher.url)
                                if watcher.one_shot:
                                    watcher.enabled = False
                                    single_update_str = "\nTo enable the next update, please manually re-enable the watcher with\n/start {0}".format(
                                        watcher.name)
                                    message += single_update_str
                                print_tag(LOG, "updated watcher {0}: change saved!".format(watcher.name))
                                watcher.send_message(message)
                            else:
                                print_tag(LOG, "watcher {0} checked -> no changes".format(watcher.name))
                                print_tag(LOG, "checked every running watcher")
                except Exception as e:
                    print_tag(LOG, e, file=sys.stderr)
        # release lock
        watchers_lock.release()
        # wait for next iteration
        flush()
        time.sleep(TIMER)
