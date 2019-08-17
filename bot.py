import time
from threading import Thread

from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler

from WatcherManager import WatcherManager
from Watcher import Watcher, Selector

file = open("token.txt", "r")
TOKEN = file.read()
file.close()

watcher_manager = WatcherManager()


def set_function(bot: Bot, update: Update):
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


def del_function(bot: Bot, update):
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


def clear_function(bot: Bot, update):
    chat_id = update.message.chat_id
    watcher_manager.clear_watcher(chat_id)
    bot.send_message(chat_id=chat_id, text="All notifiers are deleted")


def list_function(bot: Bot, update):
    chat_id = update.message.chat_id
    watchers = watcher_manager.get_watchers(chat_id)
    if len(watchers) > 0:
        text = ""
        for watcher in watchers:
            text += str(watcher) + "\n"
    else:
        text = "No notifiers available"
    bot.send_message(chat_id=chat_id, text=text)


def start_function(bot, update):
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


def stop_function(bot, update):
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


def backup():
    while True:
        time.sleep(60)
        watcher_manager.save_watchers()


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
print("Bot started!")

# start idle
updater.idle()

