import time
from threading import Thread

from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler

from WatcherManager import WatcherManager
from Watcher import Watcher, Selector
from utils import TAG, flush

file = open("token.txt", "r")
TOKEN = file.read().strip()
file.close()

watcher_manager = WatcherManager()


def set_function(bot: Bot, update: Update):
    print(TAG(), "called set: ", update.message)
    chat_id = update.message.chat_id
    args = update.message.text.split(" ")
    if len(args) < 2:
        bot.send_message(chat_id=chat_id, text="Invalid message. Command pattern is:")
        bot.send_message(chat_id=chat_id, text="/set name URL [CSS SELECTOR]")
        return

    name, url = args[1], args[2]
    watcher = Watcher(name, url, update)
    if len(args) > 3:
        watcher.selector = " ".join(args[3:])
        watcher.type = Selector.CSS
    else:
        watcher.type = Selector.NONE
    ok = watcher_manager.add_watcher(chat_id, watcher)
    if ok:
        bot.send_message(chat_id=chat_id, text="Notifier {0} correctly created! (SELECTOR: '{1}' ({2}))"
                         .format(watcher.name, watcher.selector, watcher.type))
        print("{0}: watcher {1} created.".format(chat_id, name))
    else:
        bot.send_message(chat_id=chat_id, text="Notifier {0} already exists. Please delete it".format(name))

    flush()


def del_function(bot: Bot, update):
    print(TAG(), "called del: ", update.message)
    chat_id = update.message.chat_id
    args = update.message.text.split(" ")
    if len(args) < 2:
        bot.send_message(chat_id=chat_id, text="Invalid message. Command pattern is:")
        bot.send_message(chat_id=chat_id, text="/del notifierName")
        return

    name = args[1]
    ok = watcher_manager.delete_watcher(chat_id, name)
    if ok:
        bot.send_message(chat_id=chat_id, text="Notifier {0} deleted!".format(name))
    else:
        bot.send_message(chat_id=chat_id, text="Notifier {0} not found.".format(name))

    flush()


def clear_function(bot: Bot, update):
    print(TAG(), "called clear: ", update.message)
    chat_id = update.message.chat_id
    watcher_manager.clear_watcher(chat_id)
    bot.send_message(chat_id=chat_id, text="All notifiers are deleted")

    flush()


def list_function(bot: Bot, update):
    print(TAG(), "called list: ", update.message)
    chat_id = update.message.chat_id
    watchers = watcher_manager.get_watchers(chat_id)
    if len(watchers) > 0:
        text = ""
        for watcher in watchers:
            text += str(watcher) + "\n"
    else:
        text = "No notifiers available"
    bot.send_message(chat_id=chat_id, text=text)

    flush()


def start_function(bot, update):
    print(TAG(), "called start: ", update.message)
    chat_id = update.message.chat_id
    args = update.message.text.split(" ")
    if len(args) > 1:
        name = args[1]
        ok = watcher_manager.start_watcher(chat_id, name)
        if ok == "started":
            bot.send_message(chat_id=chat_id, text="The notifier {0} now is running".format(name))
        elif ok == "already":
            bot.send_message(chat_id=chat_id, text="The notifier {0} is already running".format(name))
        else:
            bot.send_message(chat_id=chat_id, text="The notifier {0} doesn't exist".format(name))
    else:
        bot.send_message(chat_id=chat_id, text="Insert the notifier name that you want to start")

    flush()


def stop_function(bot, update):
    print(TAG(), "called stop: ", update.message)
    chat_id = update.message.chat_id
    args = update.message.text.split(" ")
    if len(args) > 1:
        name = args[1]
        ok = watcher_manager.stop_watcher(chat_id, name)
        if ok == "stopped":
            bot.send_message(chat_id=chat_id, text="The notifier {0} now is stopped".format(name))
        elif ok == "already":
            bot.send_message(chat_id=chat_id, text="The notifier {0} is already stopped".format(name))
        else:
            bot.send_message(chat_id=chat_id, text="The notifier {0} doesn't exist".format(name))
    else:
        bot.send_message(chat_id=chat_id, text="Insert the notifier name that you want to start")

    flush()


def backup():
    while True:
        time.sleep(60)
        print(TAG(), "thread_backup:", "START BACKUP ROUTINE")
        watcher_manager.save_watchers()
        print(TAG(), "thread_backup:", "BACKUP COMPLETED")

        flush()


updater = Updater(token=TOKEN)
updater.dispatcher.add_handler(CommandHandler('set', set_function))
updater.dispatcher.add_handler(CommandHandler('del', del_function))
updater.dispatcher.add_handler(CommandHandler('clear', clear_function))
updater.dispatcher.add_handler(CommandHandler('list', list_function))
updater.dispatcher.add_handler(CommandHandler('start', start_function))
updater.dispatcher.add_handler(CommandHandler('stop', stop_function))

# set watchers backup
t = Thread(target=backup)
t.start()

# start watchers thread
watcher_manager.start()

# start telegram
updater.start_polling()
print(TAG(), "Bot started!")

flush()

# start idle
updater.idle()

