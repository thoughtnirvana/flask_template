# vim: set fileencoding=utf-8 :
"""
Misc. utilities.
"""

def set_trace():
    """
    Wrapper for ``pdb.set_trace``.
    """
    from flask import current_app
    if not current_app.debug: return
    try:
        import ipdb
        ipdb.set_trace()
    except ImportError:
        import pdb
        pdb.set_trace()
