# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)
import inspect
import pdb
import sys


class Debugger(pdb.Pdb):
    """Modified debugger that assumes the existence of predefined break points."""

    def set_trace(self, frame=None):
        """See https://github.com/python/cpython/blob/b02774f42108aaf18eb19865472c8d5cd95b5f11/Lib/bdb.py#L319-L332"""
        self.reset()

        if frame is None:
            frame = sys._getframe().f_back

        while frame:
            frame.f_trace = self.trace_dispatch
            self.botframe = frame
            frame = frame.f_back

        # Automatically proceed to next break point
        self.set_continue()

        sys.settrace(self.trace_dispatch)


def debug_function(f, place='start', args=(), kwargs=None):
    if kwargs is None:
        kwargs = {}

    file_name = inspect.getfile(f)
    lines, def_line = inspect.getsourcelines(f)

    if place == 'end':
        line_num = def_line + len(lines) - 1
    else:
        line_num = def_line + 1

    debugger = Debugger()
    debugger.set_break(file_name, line_num)
    debugger.set_trace()

    f(*args, **kwargs)
