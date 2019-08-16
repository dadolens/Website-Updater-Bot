import joblib

import Watcher


class WatcherManager:
    browser = None

    def __init__(self):
        self.watchers: dict = {}        # chat-id -> list of watchers

    def add_watcher(self, chat_id, watcher: Watcher):
        if chat_id in self.watchers:
            l: list = self.watchers[chat_id]
            ok = True
            for w in l:
                if w.name == watcher.name:
                    ok = False
            if ok:
                l.append(watcher)
                watcher.start()
                return True
            return False
        else:
            self.watchers[chat_id] = [watcher]
            return True

    def delete_watcher(self, chat_id, watcher_name):
        if chat_id in self.watchers:
            l: list = self.watchers[chat_id]
            for watcher in l:
                if watcher.name == watcher_name:
                    if watcher.isRunning:
                        watcher.stop()
                    pos = l.index(watcher)
                    del l[pos]
                    return True
        return False

    def clear_watcher(self, chat_id):
        if chat_id in self.watchers:
            for watcher in self.watchers[chat_id]:
                if watcher.isRunning:
                    watcher.stop()
            self.watchers[chat_id].clear()

    def get_watchers(self, chat_id):
        if chat_id in self.watchers:
            return self.watchers[chat_id]
        else:
            return []

    def start_watcher(self, chat_id, watcher_name):
        if chat_id in self.watchers:
            for watcher in self.watchers[chat_id]:
                if watcher.name == watcher_name:
                    if not watcher.isRunning:
                        watcher.start()
                        return "started"
                    else:
                        return "already"
        return "not exist"

    def stop_watcher(self, chat_id, watcher_name):
        if chat_id in self.watchers:
            for watcher in self.watchers[chat_id]:
                if watcher.name == watcher_name:
                    if watcher.isRunning:
                        watcher.stop()
                        return "stopped"
                    else:
                        return "already"
        return "not exist"

    def save_watcher(self):
        joblib.dump(self.watchers, "watchers.pkl")

    def load_watcher(self):
        try:
            self.watchers = joblib.load("watchers.pkl")
        except Exception as e:
            print("No watchers found on disk. Clean start")

    def restart(self):
        for watchers in self.watchers.values():
            for watcher in watchers:
                if watcher.isRunning:
                    watcher.start()
