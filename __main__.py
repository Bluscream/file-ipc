from sys import argv
from time import sleep
from src.FileIPC import FileIPC
from pathlib import Path

testfile = Path(r'C:\Users\blusc\AppData\Roaming\PopstarDevs\2Take1Menu\scripts\request.ipc')
testfile_disabled = Path(r'C:\Users\blusc\AppData\Roaming\PopstarDevs\2Take1Menu\request.ipc')

def toggleFile(disable: bool = False):
    src = testfile if disable else testfile_disabled
    dst = testfile_disabled if disable else testfile
    try:
        dst.unlink(missing_ok=True)
        src.rename(dst)
    except Exception as ex: print(ex)

# toggleFile(True)

if __name__ == "__main__":
    path = argv[1] if len(argv) > 1 else '.'  
     
    ipc = FileIPC()
    
    # toggleFile()
    
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        ipc.stop()

toggleFile(True)
        
    