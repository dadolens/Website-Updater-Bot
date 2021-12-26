from enum import Enum


class Selector(Enum):
    CSS = 1
    NONE = 2


class Browser(Enum):
    FIREFOX = "Firefox"
    CHROME = "Chrome"
    CHROMIUM = "Chromium"
    EDGE = "Edge"
    OPERA = "Opera"
