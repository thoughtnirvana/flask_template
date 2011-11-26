"""
Default settings supported by Flask. Additional keys can be put
in here which will be accessible in `app.config` dictionary like
object.
"""
import sys
import os
from lib.middlewares import MethodRewriteMiddleware

DEBUG = False
TESTING = False
#: Enable CSRF. Might not be needed if WTForms is used.
CSRF_ENABLED = True
#: Key for CSRF.
CSRF_SESSION_KEY = '\x126S{\x94\xbf}o5YE\xac\x17\x8e8^_\x18z\x08\xf3z1\x97'
#: Session signing key.
SECRET_KEY = '\x18[F;(\x99\xbcF\xc8\xe3\xb5\x89R\xb7[\x17H\x85\xd8\xa9,\xbf\x95\xb4;\xe1\x80\x872+\x82\x93'
#: List of blueprints to be registered with the main wsgi app.
BLUEPRINTS = []

#: Before request middlewares.
BEFORE_REQUESTS = []

#: After request middlewares.
AFTER_REQUESTS = []

#: Middlewares to enable.
#: Middlewares are executed in the order specified.
MIDDLEWARES = [
    #: Emulate RESTFul API for client that dont' directly
    #: support REST.
    # (middleware, *args, **kwargs)
    MethodRewriteMiddleware,
]

#: Custom log handlers.
LOG_HANDLERS = []

#: Jinja2 filters.
#TEMPLATE_FILTERS = [('custom_reverse', lambda x: x[::-1])]
TEMPLATE_FILTERS = []

#: Jinja2 context processors.
#CONTEXT_PROCESSORS = [lambda: dict(user='rahul')]
CONTEXT_PROCESSORS = []

# Load appropriate settings.
environ = os.environ.get('FLASK_ENV')
# Set environment specific settings.
if environ:
    _this_module = sys.modules[__name__]
    try:
        _m = __import__('%s_settings.py' % environ)
    except ImportError, ex:
        pass
    else:
        for _k in dir(_m):
            setattr(_this_module, _k, getattr(_m, _k))
# Dev is the default environment.
else:
    try:
        from dev_settings import *
    except ImportError, ex:
        pass
