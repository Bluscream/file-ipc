from pathlib import Path
from os import getenv, path, access, R_OK
from typing import Any
from dataclasses import dataclass
from enum import Enum, auto
from logging import info, error, warning, debug


class IPCFileType(Enum):
    UNKNOWN = auto()
    COMMANDS = auto()
    PYTHON_CODE = auto()
    JSON = auto()
    @staticmethod
    def from_string(string):
        return IPCFileType.__dict__[string]
        
class IPCFileMode(Enum):
    UNKNOWN = auto()
    CREATE = auto()
    OVERWRITE = auto()
    APPEND = auto()
    @staticmethod
    def from_string(string):
        return IPCFileMode.__dict__[string]

@dataclass
class IPCFile:
    path: Path
    type: IPCFileType
    mode: IPCFileMode

    def check(self):
        if self.path.parent.exists() or access(self.path.parent, R_OK): return True
        return False

    @staticmethod
    def from_dict(obj: Any) -> 'IPCFile':
        _path = Path(path.expandvars(str(obj.get("path"))))
        _type = IPCFileType.from_string(str(obj.get("type")))
        _mode = IPCFileMode.from_string(str(obj.get("mode")))
        return IPCFile(_path, _type, _mode)

@dataclass
class IPCRequestFile(IPCFile):
    def acknowledge(self):
        self.path.unlink()
        info("%s > Acknowledged IPC request from %s", self.__class__.__name__, self.path)
@dataclass
class IPCResponseFile(IPCFile):
    pass

@dataclass
class IPCPath:
    request: IPCRequestFile
    response: IPCResponseFile

    @staticmethod
    def from_dict(obj: Any) -> 'IPCPath':
        _request = IPCRequestFile.from_dict(obj.get("request"))
        _response = IPCResponseFile.from_dict(obj.get("response"))
        return IPCPath(_request, _response)

# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)
