from dataclasses import dataclass
from enum import Enum, auto
from logging import info
from os import path, access, R_OK
from pathlib import Path
from typing import Any


class IPCFileType(Enum):
    UNKNOWN = auto()
    COMMANDS = auto()
    PYTHON = auto()
    JSON = auto()
    OS = auto()

    @staticmethod
    def from_string(string):
        string = string.upper()
        return IPCFileType.__dict__[string]
        
class IPCFileMode(Enum):
    UNKNOWN = auto()
    CREATE = auto()
    OVERWRITE = auto()
    APPEND = auto()
    @staticmethod
    def from_string(string):
        string = string.upper()
        return IPCFileMode.__dict__[string]

@dataclass
class IPCFile:
    file: Path = None
    type: IPCFileType = None
    mode: IPCFileMode = None
    def __init__(self, obj: Any):
        self.file = Path(path.expandvars(str(obj.get("path"))))
        if not obj.get("type"):
            self.type = IPCFileType.UNKNOWN
        else:
            self.type = IPCFileType.from_string(str(obj.get("type")))
        if not obj.get("mode"):
            self.mode = IPCFileMode.UNKNOWN
        else:
            self.mode = IPCFileMode.from_string(str(obj.get("mode")))
    def __repr__(self):
        return f"\"{self.file}\" ({self.type.name}, {self.mode.name})"
    def check(self):
        if self.file.parent.exists() or access(self.file.parent, R_OK): return True
        return False

class IPCRequestFile(IPCFile):
    def acknowledge(self):
        self.file.unlink()
        info("%s > Acknowledged IPC request from %s", self.__class__.__name__, self.file)
class IPCResponseFile(IPCFile):
    pass

@dataclass
class IPCPath:
    request: IPCRequestFile
    response: IPCResponseFile
    def same_dir(self):
        return self.request.file.parent == self.response.file.parent
    def __repr__(self):
        return f"{self.request} -> {self.response}"
    @staticmethod
    def from_dict(obj: Any) -> 'IPCPath':
        _request = IPCRequestFile(obj.get("request"))
        _response = IPCResponseFile(obj.get("response"))
        return IPCPath(_request, _response)
# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)
