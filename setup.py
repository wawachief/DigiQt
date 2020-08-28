# Author: Olivier Lécluse
# License GPL-3

import sys
from cx_Freeze import setup, Executable
from configparser import ConfigParser

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["os", "pyside2", "serial", "configparser"],
    "include_files": ["cli/", "assets/", "examples/", "src/", "README.md", "LICENSE"],
    "excludes": []
}

bdist_msi_options = {
    "upgrade_code": "{731A0BB3-7F97-4A2F-B7B2-939DE5A08C64}",
    "all_users": True,
    "initial_target_dir": "c:\DigiQt"
}
base = None
if sys.platform == "win32":
    base = "Win32GUI"

config = ConfigParser()
config.read("src/config.ini")

setup(  name = "DigiQt",
        version = config.get('main', 'app_version'),
        description = "Digirule2 assembler and simulator",
        author="Olivier Lecluse - Thomas Lecluse",
        options = {"build_exe": build_exe_options, "bdist_msi": bdist_msi_options},
        executables = [Executable("main.py", base=base)])
