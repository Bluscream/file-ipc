from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [], 'excludes': []}

import sys
base = 'Win32Service' if sys.platform=='win32' else None

executables = [
    Executable('__main__.py', base=None, target_name = 'FileIPC')
]

setup(name='FileIPC',
      version = '1.0.0',
      description = 'File-based Inter-process communication',
      options = {'build_exe': build_options},
      executables = executables)
