from logging import basicConfig, info, error
from logging import INFO as LOGLEVEL_INFO
from logging import DEBUG as LOGLEVEL_DEBUG
from src.IPCPaths import IPCPathsWatcher
from src.FileIPCWatcher import FileIPCWatcher
from src.IPCPath import IPCPath

class FileIPC():
    pathswatcher: IPCPathsWatcher
    watchers: list[FileIPCWatcher] = []
    
    def __init__(self) -> None:
        basicConfig(level=LOGLEVEL_INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        self.pathswatcher = IPCPathsWatcher()
        self.create()
        self.start()
    
    def create(self):
        ipcpath: IPCPath
        for ipcpath in self.pathswatcher.paths:
            self.watchers.append(FileIPCWatcher(ipcpath))
            # try:
            # except Exception as ex: error("[ERROR] %s > Failed to create watcher for %s (%s)", self.__class__.__name__, ipcpath, ex)
        info("%s > Created new instance with %i watchers", self.__class__.__name__, len(self.watchers))
    
    def start(self): info("%s > Started", self.__class__.__name__)
    def stop(self): pass