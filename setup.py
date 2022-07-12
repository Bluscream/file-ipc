import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
build_exe_options = {}

# base="Win32GUI" should be used only for Windows GUI app
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="FileIPC",
    version="1.0.0",
    description="File-Based Inter-Process Communication",
    options={"build_exe": build_exe_options},
    executables=[Executable("__main__.py")],
)