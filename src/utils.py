import sys
from datetime import datetime


def print_tag(*args, file=sys.stdout):
    return print(str(datetime.now()) + ": ", *args, file=file)


def flush():
    sys.stdout.flush()
    sys.stderr.flush()
