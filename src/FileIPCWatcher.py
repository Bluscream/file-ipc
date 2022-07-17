import subprocess
from logging import info, error, debug
from pathlib import Path
from pprint import pformat
from time import sleep

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from src.IPCPath import IPCFileType
from src.IPCPaths import IPCPath
from src.commands import commands


# class IPCRequestWatcher(IPCRequestFile):
#     def __init__(self):
#         super.__call__()
#     pass
#
# class IPCResponseWatcher(IPCResponseFile):
#     pass


class FileIPCWatcher():
    path: IPCPath
    observer: Observer
    event_handler: FileSystemEventHandler
    working = False
    queue = []
    delay_ms = 100
    eval_template =\
"""%s"""
    
    def __init__(self, path: IPCPath) -> None:
        super.__call__() # Todo
        info("%s > Initializing FileIPCWatcher for %s", self.__class__.__name__, path)
        self.create(path)
        self.start()
    
    def create(self, path: IPCPath):
        self.path = path
        self.observer = Observer()
        self.event_handler = FileSystemEventHandler()
        self.event_handler.on_created = self.on_created
        self.event_handler.on_deleted = self.on_deleted
        # self.event_handler.on_modified = self.on_modified
        self.observer.schedule(self.event_handler, path.request.file.parent, recursive=False) # Todo multiple
        info("%s > Created observer for %s", self.__class__.__name__, path)
        
    def start(self):
        self.observer.start()
        if self.path.request.file.exists(): self.handle_ipc()
    def stop(self):
        self.observer.stop()
        self.observer.join()
        
    def handle_ipc(self):
        if self.working: return
        self.working = True
        try:
            request = None
            with self.path.request.file.open("r") as f:
                request = f.read().strip()
            if not request: return
            response = None
            info("%s > Parsed IPC request from %s", self.__class__.__name__, self.path.request)
            debug("\"%s\"", request)
            self.path.request.acknowledge()
            # debug("self.path.request.type:", self.path.request.type.name, "==", IPCFileType.PYTHON.name, ":", self.path.request.type == IPCFileType.PYTHON)
            match self.path.request.type.name:
                case IPCFileType.PYTHON.name:
                    try:
                        info("%s > Evaluating PYTHON request from %s", self.__class__.__name__, self.path.request)
                        response = eval(request)  # self.eval_template.format(request)
                    except:
                        info("%s > Executing PYTHON request from %s", self.__class__.__name__, self.path.request)
                        ret = None;
                        globals = {ret: ""};
                        locals = {ret: ""}
                        # with open(self.path.request.file, "rb") as source_file:
                        #     code = compile(source_file.read(), self.path.request.file, "exec")
                        exec(request, globals, locals)
                        try:
                            response = globals["ret"] or locals["ret"]
                            debug("=== GLOBALS START ===" + "\n" + pformat(globals) + "\n" + "=== GLOBALS END ===")
                            debug("=== LOCALS START ===" + "\n" + pformat(locals) + "\n" + "=== LOCALS END ===")
                        except Exception as ex:
                            error(ex)
                case IPCFileType.COMMANDS.name:
                    info("%s > Executing COMMAND request from %s", self.__class__.__name__, self.path.request)
                    response = commands.handle(request)
                case IPCFileType.OS.name:
                    info("%s > Executing OS request from %s", self.__class__.__name__, self.path.request)
                    response = subprocess.check_output(request, shell=True).decode("utf-8")
                case _:
                    error("UNKNOWN IPC request type: %s", self.path.request.type.name)
            with self.path.response.file.open("w") as f:
                f.write(str(response).strip())
            if self.queue and len(self.queue) > 0: self.handle_ipc(self.queue.pop(0))
        except Exception as ex:
            error("%s > Error handling IPC request from %s (%s)", self.__class__.__name__, self.path.request, ex)
            self.path.request.file.exists() and self.path.request.file.unlink()
        self.working = False

    def on_created(self, event):
        file = Path(event.src_path)
        if file == self.path.request.file:
            info("%s > Recieved new IPC Request from %s, processing in %ims", self.__class__.__name__, file, self.delay_ms)
            sleep(self.delay_ms / 1000)
            self.handle_ipc()
        elif file == self.path.response.file:
            info("%s > %s has been created", self.__class__.__name__, self.path.response)
    def on_deleted(self, event):
        file = Path(event.src_path)
        if file == self.path.request.file:
            info("%s > %s has been deleted", self.__class__.__name__, self.path.request)
        elif file == self.path.response.file:
            info("%s > IPC Response acknowledged from %s", self.__class__.__name__, self.path.response)
    def on_modified(self, event):
        file = Path(event.src_path)
        info("%s > %s has been modified", self.__class__.__name__, file)