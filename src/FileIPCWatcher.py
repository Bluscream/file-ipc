from time import sleep
from logging import info, error, warning, debug
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from src.IPCPath import IPCRequestFile, IPCResponseFile
from src.IPCPaths import IPCPath

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
        if self.path.request.file.exists(): self.handle_ipc(self.path.request)
    def stop(self):
        self.observer.stop()
        self.observer.join()
        
    def handle_ipc(self):
        if self.working: return
        self.working = True
        try:
            request = None
            with self.path.request.file.open("r") as f: request = f.read().strip()
            if not request: return
            response = None
            info("%s > Parsed IPC request from %s", self.__class__.__name__, self.path.request)
            debug("\"%s\"", request)
            self.path.request.file.unlink()
            info("%s > Acknowledged IPC request from %s", self.__class__.__name__, self.path.request)
            try: response = eval(request) # self.eval_template.format(request)
            except:
                ret = None; globals = {"ret": ""}; locals = {}
                with open(self.path.request.file, "rb") as source_file:
                    code = compile(source_file.read(), self.path.request.file, "exec")
                exec(code, globals, locals)
                # print("=== GLOBALS START ===")
                # try: pprint.pprint(globals)
                # except Exception as ex: print(ex)
                # print("=== LOCALS END ===")
                # print("=== LOCALS START ===")
                # try: pprint.pprint(locals)
                # except Exception as ex: print(ex)
                # print("=== LOCALS END ===")
                try: response = locals["ret"] # if hasattr(locals, "files"):
                except Exception as ex: print(ex) 
            with self.path.response.file.open("w") as f:
                f.write(str(response).strip())
            if self.queue and len(self.queue) > 0: self.handle_ipc(self.queue.pop(0))
        except Exception as ex:
            error("%s > Error handling IPC request from %s (%s)", self.__class__.__name__, self.path.request, ex)
            self.path.request.file.unlink()
        self.working = False

    def on_created(self, event):
        file = Path(event.src_path)
        if file == self.path.request.file:
            info("%s > Recieved new IPC Request from %s, processing in %ims", self.__class__.__name__, file, self.delay_ms)
            sleep(self.delay_ms / 1000)
            self.handle_ipc(file)
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