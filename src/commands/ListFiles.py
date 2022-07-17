from logging import info
from os import path
from pathlib import Path


class ListFiles:
    @staticmethod
    def handle(dir: str, pattern: str):
        info("commands:listdir > dir %s pattern %s", dir, pattern)
        ret = ""
        for file in Path(path.expandvars(dir.strip())).glob(pattern):
            ret += path.basename(file.name) + "\n"
        return ret
