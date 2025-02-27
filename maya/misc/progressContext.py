# -*- coding: utf-8 -*-
"""
https://stackoverflow.com/questions/29708445/how-do-i-make-a-contextmanager-with-a-loop-inside
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2021-05-13 21:27:57"


from maya import cmds
import traceback


def progress(seq, status="", title=""):
    cmds.progressWindow(status=status, title=title, progress=0.0, isInterruptable=True)
    total = len(seq)
    for i, item in enumerate(seq):
        try:
            if cmds.progressWindow(query=True, isCancelled=True):
                break
            cmds.progressWindow(e=True, progress=float(i) / total * 100)
            yield item  # with body executes here
        except:
            traceback.print_exc()
            cmds.progressWindow(ep=1)
    cmds.progressWindow(ep=1)

if __name__ == "__main__":
    for i in progress(range(5000)):
        print(i)
