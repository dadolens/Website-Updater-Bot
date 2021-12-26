import time
from threading import Thread

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

from Watcher import Watcher, Selector
from WatcherManager import WatcherManager
from config import TOKEN, BACKUP_TIMER, logger
from utils import flush

watcher_manager = WatcherManager()


def set_function(update: Update, context: CallbackContext):
    logger.info("called set: " + update.message)
    chat_id = update.message.chat_id
    args = update.message.text.split(" ")
    if len(args) < 3:
        update.message.reply_text("Invalid message. Command pattern is:")
        update.message.reply_text("/set name URL (single|continue) [CSS SELECTOR]")
        return

    name, url, one_shot = args[1], args[2], args[3]
    watcher = Watcher(name, url, one_shot == 'single', update.message.chat_id)
    if len(args) > 4:
        watcher.selector = " ".join(args[4:])
        watcher.type = Selector.CSS
    else:
        watcher.type = Selector.NONE

    ok = watcher_manager.add_watcher(chat_id, watcher)
    if ok:
        update.message.reply_text("Notifier {0} correctly created! (SELECTOR: '{1}' ({2}))"
                                  .format(watcher.name, watcher.selector, watcher.type))
        logger.info("{0}: watcher {1} created.".format(chat_id, name))
    else:
        update.message.reply_text("Notifier {0} already exists. Please delete it".format(name))

    flush()


def del_function(update: Update, context: CallbackContext):
    logger.info("called del: " + update.message)
    chat_id = update.message.chat_id
    args = update.message.text.split(" ")
    if len(args) < 2:
        update.message.reply_text("Invalid message. Command pattern is:")
        update.message.reply_text("/del notifierName")
        return

    name = args[1]
    ok = watcher_manager.delete_watcher(chat_id, name)
    if ok:
        update.message.reply_text("Notifier {0} deleted!".format(name))
    else:
        update.message.reply_text("Notifier {0} not found.".format(name))

    flush()


def clear_function(update: Update, context: CallbackContext):
    logger.info("called clear: " + update.message)
    chat_id = update.message.chat_id
    watcher_manager.clear_watcher(chat_id)
    update.message.reply_text("All notifiers are deleted")

    flush()


def list_function(update: Update, context: CallbackContext):
    logger.info("called list: " + update.message)
    chat_id = update.message.chat_id
    watchers = watcher_manager.get_watchers(chat_id)
    if len(watchers) > 0:
        text = ""
        for watcher in watchers:
            text += str(watcher) + "\n"
    else:
        text = "No notifiers available"
    update.message.reply_text(text)

    flush()


def start_function(update: Update, context: CallbackContext):
    logger.info("called start: " + update.message)
    chat_id = update.message.chat_id
    args = update.message.text.split(" ")
    if len(args) > 1:
        name = args[1]
        ok = watcher_manager.start_watcher(chat_id, name)
        if ok == "started":
            update.message.reply_text("The notifier {0} now is running".format(name))
        elif ok == "already":
            update.message.reply_text("The notifier {0} is already running".format(name))
        else:
            update.message.reply_text("The notifier {0} doesn't exist".format(name))
    else:
        update.message.reply_text("Insert the notifier name that you want to start")

    flush()


def stop_function(update: Update, context: CallbackContext):
    logger.info("called stop: " + update.message)
    chat_id = update.message.chat_id
    args = update.message.text.split(" ")
    if len(args) > 1:
        name = args[1]
        ok = watcher_manager.stop_watcher(chat_id, name)
        if ok == "stopped":
            update.message.reply_text("The notifier {0} now is stopped".format(name))
        elif ok == "already":
            update.message.reply_text("The notifier {0} is already stopped".format(name))
        else:
            update.message.reply_text("The notifier {0} doesn't exist".format(name))
    else:
        update.message.reply_text("Insert the notifier name that you want to start")

    flush()


def backup():
    while True:
        time.sleep(BACKUP_TIMER)
        logger.info("thread_backup: START BACKUP ROUTINE")
        watcher_manager.save_watchers()
        logger.info("thread_backup: BACKUP COMPLETED")
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
logger.info("Bot started!")

flush()

# start telegram bot idle
updater.idle()
