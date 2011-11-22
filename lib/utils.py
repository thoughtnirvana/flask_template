# vim: set fileencoding=utf-8 :
"""
Misc. utilities.
"""
import sys


def set_trace():
    """
    Wrapper for ``pdb.set_trace``.
    Restore ``stdin``, ``stdout`` and ``stderr``.
    """
    from flask import current_app
    if not current_app.debug: return
    try:
        import ipdb as pdb
    except ImportError:
        import pdb
    debugger = pdb.Pdb(stdin=sys.__stdin__,
                       stdout=sys.__stderr__)
    debugger.set_trace(sys._getframe().f_back)
