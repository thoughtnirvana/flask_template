#!/usr/bin/env python
"""
Implements the main WSGI app. It instantiates and sets it up. It can
be run stand-alone as a flask application or it can be imported and
the resulting `app` object be used.
"""
# Set lib path.
import sys, os
lib_dir = os.path.join(os.path.dirname(__file__), 'lib')
if lib_dir not in sys.path:
    sys.path.insert(0, lib_dir)
#: stdlib imports
import datetime
#: 3rd party imports
from flask import Flask, request, g, redirect, url_for
from flaskext.babel import Babel
from flaskext.cache import Cache
from flaskext.sqlalchemy import SQLAlchemy
import gaesessions
#: Project imports.
import urls
from common.middlewares import MethodRewriteMiddleware
from apps.sample.models import User
import shared


# Configuration variables.

#: List of modules to be registered with the main wsgi app.
#: For app engine, it should be None. Modules are registered
#: when used.
modules = ()
#: The .py file containing the configurations for Flask framework.
#: It should be in sys.path or PYTHONPATH.
config_object = 'settings'
#: Name for the main `app`. Mainly used for debugging.
app_name = 'sample'
#: Key for signing cookies.
GAE_SECRET_KEY = "N\r\xb2\x18\x16xB9\x8b\x94G\x1cs\xb4\x9b'S\xd9\x83\xe8\x9f\xd6x*\xc9R\xe1\xc8r'q\t\xe0\xeb\xae\\\xab\xc9\x93\xce#\x0efo\xf9\xba\xcel#=_d\xa4\xf7\xc3p1\xa3J8\xa6\xb9\x16"
#: Middlewares to enable.
#: Middlewares are executed in the order specified.
middlewares = [
    #: Emulate RESTFul API for client that dont' directly
    #: support REST.
    (MethodRewriteMiddleware, [], {}),
    # :Session middleware.
    (gaesessions.SessionMiddleware, [],
    {'cookie_key': GAE_SECRET_KEY,
     'cookie_only_threshold': 0,
     'lifetime': datetime.timedelta(hours=6)
    }),
]


def setup_request():
    #: Assign ``sessions``.
    g.session = gaesessions.get_current_session()
    #: Init ``user``.
    g.user = None
    if g.session.get('auth_id'):
        g.user = User.get_user(g.session['auth_id'])


#: Before request middlewares.
#: Run after setting up of other middlewares.
before_requests = (setup_request, )


def init():
    """
    Sets up flask application object `app` and returns it.
    """
    # Instantiate main app, load configs, register modules, set
    # url patterns and return the `app` object.
    shared.app = app = Flask(app_name)
    app.config.from_object(config_object)
    # Init SQLAlchemy wrapper.
    shared.db = db = SQLAlchemy(app)
    # Register modules.
    for m in modules:
        app.register_module(m)
    # Add middlewares.
    for mware, args, kwargs in middlewares:
        app.wsgi_app = mware(app.wsgi_app, *args, **kwargs)
    # Register before request middlewares.
    for before in before_requests:
        before = app.before_request(before)
    # URL rules.
    urls.set_urls(app)
    #: Wrap the `app` with `Babel` for i18n.
    babel = Babel(app)
    shared.cache = Cache(app)
    return app


if __name__ == '__main__':
    #: Create the `app` object via :func:`init`. Run the `app`
    #: if called standalone.
    app = init()
    app.run()
