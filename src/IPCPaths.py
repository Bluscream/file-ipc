from os import getenv, path, access, R_OK
from logging import info
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class IPCPath():
    request_file: Path
    response_file: Path
    
    def __init__(self, *args, **kwargs):
        self.path = Path(*args, **kwargs)

    @staticmethod
    def from_line(self, line: str) -> None:
        line = line.split(";")
        ret = Path([0])
        ret.request_file = ret.joinpath(line[1] if len(line) > 1 else "request.ipc")
        ret.response_file = ret.joinpath(line[2] if len(line) > 2 else "response.ipc")
        return ret

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
        info("%s > Created observer for %s", self.__class__.__name__, self.file)
        
    def start(self):
        self.observer.start()
        info("%s > Watching for changes in %s", self.__class__.__name__, self.file)
    
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
                count = 0
                for line in f: # f.read().splitlines()
                    count += 1
                    line = IPCPath(path.expandvars(line.strip()))
                    if line.exists() or access(line.parent, R_OK):
                        paths.append(line)
                        info("%s > paths[%i] %s", self.__class__.__name__, count, line)
                    else: info("%s > Path %s does not exist, ignoring", self.__class__.__name__, line)
        # self.paths = paths
        info("%s > Loaded %i paths from %s", self.__class__.__name__, len(paths), file)
        return paths
            
    def save(self, file=None, paths=None):
        file = file or self.file
        paths = paths or self.paths
        with file.open("w") as f:
            f.write("\n".join(paths))