import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["os", "pyside2", "serial", "ConfigParser"],
    "include_files": ["cli/", "assets/", "examples/", "src/", "README.md", "LICENSE"],
    "excludes": []
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"
    if 'bdist_msi' in sys.argv:
        sys.argv += ['--initial-target-dir', 'c:\DigiQt']

setup(  name = "DigiQt",
        version = "1.0.beta2",
        description = "Digirule2 assembler and simulator",
        author="Olivier Lecluse - Thomas Lecluse",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main.py", base=base)])
