# File Based Tool for Inter-process communication

Add your watched directories to `C:\ipc.paths` like so
```
%userprofile%\Desktop\
%appdata%\PopstarDevs\2Take1Menu\scripts\ipc
```

Let your script write your IPC messages as python code to a file called `request.ipc` in one of those paths
```py
from pathlib import Path
ret = ""
for file in Path(r'C:\Users\blusc\AppData\Roaming\PopstarDevs\ScriptHook').glob("*.asi"): ret += str(file) + "\n"
```

Read the response from `response.ipc` and delete the `request.ipc` file
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
