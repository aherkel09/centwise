import sys
from cx_Freeze import setup, Executable

include_files = ['storeBudget.txt', 'overwrite.txt']
build_exe_options = {"packages": ["os"], "includes": ["tkinter"],
                     "include_files": include_files}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Centwise",
        version = "0.0.1",
        description = "Generate Monthly Budgets",
        options = {"build_exe": build_exe_options},
        executables = [Executable("centwise.py", base=base)])
