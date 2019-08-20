# Website Updater Bot

A telegram bot that notifies when a web page (or a piece of it) change. It uses <a href="https://phantomjs.org/">PhantomJS</a>
to render web pages and search for differences from the last time it was checked.
<br>


### Requirements
This bot has some dependency. To install them, run

```bash
pip install python-telegram-bot joblib selenium --user
```
Also, for selenium, is necessary to install PhantomJS. For more information,
click <a href='https://phantomjs.org/download.html'>here</a>.
<br>
Once you have installed PhantomJS, you need to write the path to its executable in a file called ```path_phantom_js.txt```
in the main directory of the project. The file must contain <b>ONLY</b> the path. For example, ```/bin/phantomjs/phantomjs```


### Telegram Bot API Token
To make the bot works, you need to create the file ```token.txt``` in the main directory of the project and
write in it the bot api token. The file must contains <b>ONLY</b> the token and nothing else.
