# Website Updater Bot

A telegram bot that notifies when a web page (or a piece of it) change. It uses <a href="https://phantomjs.org/">PhantomJS</a>
to render web pages and search for differences from the last time it was checked.
<br>


### Requirements
This bot has some dependency. To install them, run

```bash
pip install -r requirements.txt
```
Also, for selenium, is necessary to install PhantomJS. For more information,
click <a href='https://phantomjs.org/download.html'>here</a>.
<br>
Once you have installed PhantomJS, you need to write the path to its executable in a file called ```path_phantom_js.txt```
in the main directory of the project. The file must contain <b>ONLY</b> the path. For example, ```/bin/phantomjs/phantomjs```


### Telegram Bot API Token
To make the bot works, you need to create the file ```token.txt``` in the main directory of the project and
write in it the bot api token. The file must contains <b>ONLY</b> the token and nothing else.


### Bot commands
- set: ```/set NAME URL [SELECTOR]``` create a new watcher.
    - NAME is the identifier of your watcher. It must be unique.
    - URL is the url to watch.
    - SELECTOR is the CSS selector that identifies what you want to watch in the URL page. It could represents one or more elements. If it's not provided, the bot will watch the entire web page.
- del: ```/del NAME``` delete an existing watcher.
    - NAME is the identifier of the watcher that you want to delete.
- clear: ```/clear``` delete all the existing watchers.
- list: ```/list``` show the list of all the existing watchers and their information.
- start: ```/start NAME``` start a stopped watcher.
    - NAME is the identifier of the watcher that you want to start.
- stop: ```/stop NAME``` stop a running watcher.
    - NAME is the identifier of the watcher that you want to stop.

