from logging import basicConfig, info, error
from logging import INFO as LOGLEVEL_INFO
from src.IPCPaths import IPCPathsWatcher
from src.FileIPCWatcher import FileIPCWatcher

class FileIPC():
    pathswatcher: IPCPathsWatcher
    watchers: list[FileIPCWatcher] = []
    
    def __init__(self) -> None:
        basicConfig(level=LOGLEVEL_INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        self.pathswatcher = IPCPathsWatcher()
        self.create()
        self.start()
    
    def create(self):
        for path in self.pathswatcher.paths:
            try: self.watchers.append(FileIPCWatcher(path))
            except Exception as ex: error("[ERROR] %s > Failed to create watcher for %s (%s)", self.__class__.__name__, path, ex)
        info("%s > Created new instance with %i watchers", self.__class__.__name__, len(self.watchers))
    
    def start(self): info("%s > Started", self.__class__.__name__)
    def stop(self): pass