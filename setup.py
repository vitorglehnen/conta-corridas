import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["os"], "includes": ["tkinter", "pyodbc", "tkcalendar", "pandas", "tkinter.messagebox"], "include_files": ["1.ico"]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Editor de Texto",
    version="1.0",
    description="Um editor de texto personalizado",
    options={"build_exe": build_exe_options},
    executables=[Executable(script="main.py", base=base, icon='1.ico')]
)