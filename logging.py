import os
from datetime import datetime, date
from os.path import exists
from typing import TextIO
from enum import Enum

class levels(Enum):
    ERROR = 1,
    WARN = 2,
    INFO = 3,
    DEBUG = 4

def level_to_text(level) -> str:
    choices = {'[ERROR]': 1, '[WARN]': 2, '[INFO]': 3, '[DEBUG]': 4}
    return choices.get(level, '[INFO]')

class Logger():
    logfile: TextIO

    def __init__(self):
        if exists("log.txt"):
            os.remove("log.txt")
        self.logfile = open("log.txt", "a")
        self.log(f"-=-=-=-=-=-=-=- LOG START -=-=-=-=-=-=-=-")
        self.log(f"{date.today().strftime('%d/%m/%Y')}")


    def log(self,logtext,level=levels.INFO):
        self.logfile.write(f"{datetime.now().strftime('%H:%M:%S')} {level_to_text(level)}: {logtext}")
