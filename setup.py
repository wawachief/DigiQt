# Author: Olivier Lécluse
# License GPL-3

#
# Digirule CPU Core
#

import sys
from cx_Freeze import setup, Executable
from configparser import ConfigParser

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["os", "pyside2", "serial", "configparser"],
    "include_files": ["cli/", "assets/", "examples/", "src/", "README.md", "LICENSE"],
    "excludes": []
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"
    if 'bdist_msi' in sys.argv:
        sys.argv += ['--initial-target-dir', 'c:\DigiQt']

config = ConfigParser()
config.read("src/config.ini")

setup(  name = "DigiQt",
        version = config.get('main', 'app_version'),
        description = "Digirule2 assembler and simulator",
        author="Olivier Lecluse - Thomas Lecluse",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main.py", base=base)])
