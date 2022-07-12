# File Based Tool for Inter-process communication

Add your watched directories to `C:\ipc.paths` like so
```
%userprofile%\Desktop\
%appdata%\PopstarDevs\2Take1Menu\scripts\ipc
```

Let your script write your IPC messages as python code to a file called `request.ipc` in one of those paths

Read the response from `response.ipc` and delete the `request.ipc` file
