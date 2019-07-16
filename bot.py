from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler

from Watcher import Watcher, Selector
from config import TOKEN


def set_function(bot: Bot, update: Update, user_data: dict):
    chat_id = update.message.chat_id
    args = update.message.text.split(" ")
    if len(args) < 2:
        bot.send_message(chat_id=chat_id, text="Invalid message. Command pattern is:")
        bot.send_message(chat_id=chat_id, text="/set name URL [XPATH/CSS SELECTOR]")
        return

    name, url = args[1], args[2]
    if name in user_data:
        bot.send_message(chat_id=chat_id, text="Notifier {0} already exists. Please delete it".format(name))
        return
    watcher = Watcher(name, url, update)
    if len(args) > 3:
        watcher.selector = args[3]
        if '/' in watcher.selector:
            watcher.type = Selector.XPATH
        else:
            watcher.type = Selector.CSS
    else:
        watcher.type = Selector.NONE
    user_data[name] = watcher

    bot.send_message(chat_id=chat_id, text="Notifier {0} correctly created! (SELECTOR: {1})".format(watcher.name, watcher.type))


def del_function(bot: Bot, update, user_data):
    chat_id = update.message.chat_id
    args = update.message.text.split(" ")
    if len(args) < 2:
        bot.send_message(chat_id=chat_id, text="Invalid message. Command pattern is:")
        bot.send_message(chat_id=chat_id, text="/del notifierName")
        return

    name = args[1]
    if name in user_data:
        del user_data[name]
        bot.send_message(chat_id=chat_id, text="Notifier {0} deleted!".format(name))
    else:
        bot.send_message(chat_id=chat_id, text="Notifier {0} not found.".format(name))


def clear_function(bot: Bot, update, user_data: dict):
    chat_id = update.message.chat_id
    if len(user_data) > 0:
        user_data.clear()
        bot.send_message(chat_id=chat_id, text="All notifiers are deleted")
    else:
        bot.send_message(chat_id=chat_id, text="No notifiers available to be deleted")


def list_function(bot: Bot, update, user_data):
    chat_id = update.message.chat_id
    if len(user_data) > 0:
        text = ""
        for name, watcher in user_data.items():
            text += str(watcher) + "\n"
    else:
        text = "No notifiers available"
    bot.send_message(chat_id=chat_id, text=text)


updater = Updater(token=TOKEN)
updater.dispatcher.add_handler(CommandHandler('set', set_function, pass_user_data=True))
updater.dispatcher.add_handler(CommandHandler('del', del_function, pass_user_data=True))
updater.dispatcher.add_handler(CommandHandler('clear', clear_function, pass_user_data=True))
updater.dispatcher.add_handler(CommandHandler('list', list_function, pass_user_data=True))


updater.start_polling()

print("Bot started!")
updater.idle()
