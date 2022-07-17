# File Based Tool for Inter-process communication

Add your watched directories to `C:\ipc.paths` like so;
You can find a list of modes and types in

```json
[
    {
        "request": {
            "path": "%appdata%\\PopstarDevs\\2Take1Menu\\scripts\\ipc\\request.txt",
            "type": "python",
            "mode": "create"

        },
        "response": {
            "path": "%appdata%\\PopstarDevs\\2Take1Menu\\scripts\\ipc\\response.txt",
            "mode": "create"
        }
    },
    {
        "request": {
            "path": "%userprofile%\\Desktop\\request.os.ipc",
            "type": "os",
            "mode": "create"
        },
        "response": {
            "path": "%userprofile%\\Desktop\\response.os.ipc",
            "mode": "create"
        }
    }
]
```

#### Note: Currently only request and response files in the same directory are supported!

Let your script write your IPC messages as python code to a file called `request.ipc` in one of those paths

```py
from pathlib import Path
ret = ""
for file in Path(r'C:\Users\blusc\AppData\Roaming\PopstarDevs\ScriptHook').glob("*.asi"): ret += str(file) + "\n"
```

Read the response from your response file and delete the request file
```
C:\Users\blusc\AppData\Roaming\PopstarDevs\ScriptHook\blinker.asi
C:\Users\blusc\AppData\Roaming\PopstarDevs\ScriptHook\ELS.asi
C:\Users\blusc\AppData\Roaming\PopstarDevs\ScriptHook\HeapAdjuster.asi
C:\Users\blusc\AppData\Roaming\PopstarDevs\ScriptHook\J10RailroadEngineer.asi
C:\Users\blusc\AppData\Roaming\PopstarDevs\ScriptHook\Lazer.asi
C:\Users\blusc\AppData\Roaming\PopstarDevs\ScriptHook\MutedSpeechAndPain 1.1.asi
C:\Users\blusc\AppData\Roaming\PopstarDevs\ScriptHook\PackfileLimitAdjuster.asi
C:\Users\blusc\AppData\Roaming\PopstarDevs\ScriptHook\PlayerLocationDisplay.asi
C:\Users\blusc\AppData\Roaming\PopstarDevs\ScriptHook\ScriptHookVDotNet.asi
```
