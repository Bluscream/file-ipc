from sys import argv
from time import sleep
from src.FileIPC import FileIPC

if __name__ == "__main__":
    ipc = FileIPC()
    try:
        while True: sleep(1)
    except KeyboardInterrupt:
        ipc.stop()
        
    