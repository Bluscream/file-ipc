from os import getenv, path, access, R_OK
from logging import info, error
from pathlib import Path
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from src.IPCPath import IPCPath

class IPCPathsWatcher(object):
    file: Path
    paths: list[IPCPath]
    observer: Observer
    event_handler: FileSystemEventHandler
    
    def __init__(self) -> None:
        self.file = Path(getenv("SYSTEMDRIVE", "C:")).joinpath("/ipc.paths")
        self.paths = self.load()
        info("%s > Initializing IPCPathsWatcher for %s", self.__class__.__name__, self.file)
        self.create()
        self.start()
    
    def check(self, _path: Path):
        if _path != self.file: return False
        return True
    
    def create(self):
        if not self.file.exists():
            info("%s > Creating %s", self.__class__.__name__, self.file)
            self.file.touch()
        self.observer = Observer()
        self.event_handler = FileSystemEventHandler()
        self.event_handler.on_modified = self.onPathsFileModified
        self.event_handler.on_deleted = self.onPathsFileDeleted
        self.event_handler.on_created = self.onPathsFileCreated
        self.observer.schedule(self.event_handler, self.file.parent, recursive=False)
        info("%s > Created observer for \"%s\"", self.__class__.__name__, self.file)
        
    def start(self):
        self.observer.start()
        info("%s > Watching for changes in \"%s\"", self.__class__.__name__, self.file)
    
    def onPathsFileModified(self, event):
        info("%s > Paths file has been modified, reloading paths...", self.__class__.__name__)
        self.paths = self.load()
    
    def onPathsFileDeleted(self, event):
        info("%s > Paths file has been deleted, stopping...", self.__class__.__name__)
        self.stop()
    
    def onPathsFileCreated(self, event):
        info("%s > Paths file has been created, starting...", self.__class__.__name__)
        self.start()
    
    def stop(self):
        info("%s > Stopping...", self.__class__.__name__)
        self.observer.stop()
        self.observer.join()
    
    def load(self, file=None):
        file = file or self.file
        paths = []
        if file.exists():
            with self.file.open("r") as f:
                jsonstring = json.load(f)
                count = 0
                for item in jsonstring:
                    ipcpath = IPCPath.from_dict(item)
                    count += 1
                    if ipcpath.request.check() and ipcpath.response.check():
                        paths.append(ipcpath)
                        info("%s > paths[%i] %s", self.__class__.__name__, count, ipcpath)
                    else:
                        error("%s > Path %s does not exist, ignoring", self.__class__.__name__, ipcpath)
                        break
        # self.paths = paths
        info("%s > Loaded %i paths from \"%s\"", self.__class__.__name__, len(paths), file)
        return paths
            
    def save(self, file=None, paths=None):
        file = file or self.file
        paths = paths or self.paths
        raise Exception("Not implemented")