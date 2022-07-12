from time import sleep
from logging import info, error, warning, debug
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileIPCWatcher(object):
    # directory: Path
    request_file: Path
    response_file: Path
    observer: Observer
    event_handler: FileSystemEventHandler
    working = False
    queue = []
    delay_ms = 10
    eval_template =\
"""%s"""
    
    def __init__(self, dir: Path) -> None:
        info("%s > Initializing FileIPCWatcher for directory %s", self.__class__.__name__, dir)
        self.create(dir)
        self.start()
    
    def create(self, dir):
        # self.directory = dir
        self.request_file = dir.joinpath("request.ipc")
        self.response_file = dir.joinpath("response.ipc")
        self.observer = Observer()
        self.event_handler = FileSystemEventHandler()
        self.event_handler.on_created = self.on_created
        self.event_handler.on_deleted = self.on_deleted
        self.observer.schedule(self.event_handler, dir, recursive=False)
        info("%s > Created observer for %s", self.__class__.__name__, dir)
        
    def start(self): self.observer.start()
    def stop(self):
        self.observer.stop()
        self.observer.join()
        
    def handle_ipc(self, file: Path):
        self.working = True
        request = None
        with file.open("r") as f: request = f.read().strip()
        if not request: return
        response = None
        info("%s > Parsed IPC request from %s", self.__class__.__name__, file)
        debug(request)
        try: response = eval(request) # self.eval_template.format(request)
        except:
            ret = None; globals = {ret: ""}; locals = {}
            with open(file, "rb") as source_file:
                code = compile(source_file.read(), file, "exec")
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
        file.unlink()
        with self.response_file.open("w") as f:
            f.write(str(response).strip())
        info("%s > Acknowledged IPC request from %s", self.__class__.__name__, file)
        debug(response)
        if self.queue and len(self.queue) > 0: self.handle_ipc(self.queue.pop(0))
        self.working = False

    def on_created(self, event):
        file = Path(event.src_path)
        if file == self.request_file:
            info("%s > Recieved new IPC Request from %s, processing in %ims", self.__class__.__name__, file, self.delay_ms)
            sleep(self.delay_ms / 1000)
            self.handle_ipc(file)
        elif file == self.response_file:
            info("%s > %s has been created", self.__class__.__name__, file)
    def on_deleted(self, event):
        file = Path(event.src_path)
        if file == self.request_file:
            info("%s > %s has been deleted", self.__class__.__name__, file)
        elif file == self.response_file:
            info("%s > IPC Response acknowledged from %s", self.__class__.__name__, file)