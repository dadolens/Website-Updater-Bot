# Website Updater Bot

A telegram bot that notifies when a web page (or a piece of it) change. It uses Selenium Web Driver
support browser navigation and enable checks depending on js renders.
<br>


### Requirements
This bot has some dependency. To install them, run

```bash
pip install -r requirements.txt
```
The browser drivers are automatically handled by the package `webdriver-manager`.

###Configuration
Every configuration is saved in the `config.json` file, where every field must be setted with the following instructions:
- token
  - The Telegram Bot API Token. To generate one, please check the Telegram Bot documentation
- browser
  - The browser used by Selenium. It can be one of the following values:
    - FIREFOX
    - CHROME
    - CHROMIUM
    - EDGE
    - OPERA
- timer
  - The amount of seconds to wait to check if any site is changed
- backup_timer
  - The amount of seconds that passess between every run of the backup routine
- save_path
  - The path of the folder where the backup routine saves data


### Bot commands
- set: ```/set NAME URL (single|continue) [SELECTOR]``` create a new watcher.
    - `NAME` is the identifier of your watcher. It must be unique.
    - `URL` is the url to watch.
    - `single|continue` setup if the watcher still continue to check updates after the first change
    - `SELECTOR` is the CSS selector that identifies what you want to watch in the URL page. It could represents one or more elements. If it's not provided, the bot will watch the entire web page.
- del: ```/del NAME``` delete an existing watcher.
    - NAME is the identifier of the watcher that you want to delete.
- clear: ```/clear``` delete all the existing watchers.
- list: ```/list``` show the list of all the existing watchers and their information.
- start: ```/start NAME``` start a stopped watcher.
    - NAME is the identifier of the watcher that you want to start.
- stop: ```/stop NAME``` stop a running watcher.
    - NAME is the identifier of the watcher that you want to stop.

## Future updates
- Add support to PhantomJS to run the bot in a non-desktop environment
- Add /help command to print info about all the bot commands
- Add other selector, like XPath
- Add screenshot of the changed website to the notification (if requested)
- Support telegram button API to create watcher more easily and with better UX
- 