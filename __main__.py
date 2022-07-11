import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

def checkFile(path):
    return not (path.endswith("__main__.py"))

def on_created(event):
    if not checkFile(event.src_path): return
    print(f"hey, {event.src_path} has been created!")
def on_deleted(event):
    if not checkFile(event.src_path): return
    print(f"what the f**k! Someone deleted {event.src_path}!")
def on_modified(event):
    if not checkFile(event.src_path): return
    print(f"hey buddy, {event.src_path} has been modified")
def on_moved(event): pass

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = LoggingEventHandler()
    event_handler.on_created = on_created
    event_handler.on_deleted = on_deleted
    event_handler.on_modified = on_modified
    event_handler.on_moved = on_moved
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()