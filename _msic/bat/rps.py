# -*- coding: utf-8 -*-
"""
rps rez powershell command

# prefix for special command.

examples:
rps #code  -  activate env launch vscode
rps cmake maya  - activate powsershell with cmake&maya rez package
"""

# Import future modules
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2022-10-25 14:23:43"


# Import built-in modules
import logging
import os
import pathlib
import subprocess
import sys

# Import third-party modules
from rez import serialise

logging.basicConfig(level=logging.INFO)
ROOT = pathlib.Path(os.getcwd())


commands = {
    "#code": lambda requires: requires + ["--", "code", str(ROOT)],
    "#mobu": lambda requires: requires
    + ["motionbuilder-2018", "--", "motionbuilder.exe"],
}


def main():
    requires = []
    package = ROOT / "package.py"
    if package.exists():
        pkg = serialise.load_from_file(str(package))
        requires += pkg.get("requires", [])
        requires += pkg.get("build_requires", [])

    args = sys.argv[1:]
    requires += args

    for index, arg in enumerate(requires):
        if not arg.startswith("#"):
            continue
        post_args = requires[index + 1 :]
        requires = requires[:index]
        # not requires and requires.append("python")
        callback = commands.get(arg)
        requires = callback(requires) if callback else requires
        requires += post_args
        break

    command = " ".join(["rez", "env", "--shell", "powershell"] + requires)
    logging.info(command)
    subprocess.run(command)


if __name__ == "__main__":
    main()
