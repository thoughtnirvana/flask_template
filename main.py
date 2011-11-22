#!/usr/bin/env python
"""
Implements the main WSGI app. It instantiates and sets it up. It can
be run stand-alone as a flask application or it can be imported and
the resulting `app` object be used.
"""
from flask import Flask
from flaskext.babel import Babel
from flaskext.cache import Cache
from flaskext.sqlalchemy import SQLAlchemy
from flaskext.assets import Environment

import config
import config.urls as urls
import config.settings as settings

def init(basic_app=False):
    """
    Sets up flask application object `app` and returns it.
    If `basic_app` is true, it creates the app and the db object.
    Mainly useful for using models outside of the app.
    """
    # Instantiate main app, load configs, register modules, set
    # url patterns and return the `app` object.
    app = Flask(__name__)
    if not basic_app:
        app.config.from_object('config.settings')
        # Other initializations.
        for fn, values in [(set_middlewares, getattr(settings, 'MIDDLEWARES', None)),
                        (set_blueprints, getattr(settings, 'BLUEPRINTS', None)),
                        (set_before_handlers, getattr(settings, 'BEFORE_REQUESTS', None)),
                        (set_after_handlers, getattr(settings, 'AFTER_REQUESTS', None)),
                        (set_log_handlers, getattr(settings, 'LOG_HANDLERS', None)),
                        (set_context_processors, getattr(settings, 'CONTEXT_PROCESSORS', None)),
                        (set_template_filters, getattr(settings, 'TEMPLATE_FILTERS', None))]:
            if values:
                fn(app, values)
        # URL rules.
        urls.set_urls(app)
        #: Wrap the `app` with `Babel` for i18n.
        Babel(app)
        Environment(app)
        config.cache = Cache(app)
    # Init SQLAlchemy wrapper.
    config.db = SQLAlchemy(app)
    return app

def set_middlewares(app, middlewares):
    """
    Adds middlewares to the app.
    """
    # Add middlewares.
    if middlewares:
        for mware, args, kwargs in middlewares:
            app.wsgi_app = mware(app.wsgi_app, *args, **kwargs)

def set_blueprints(app, blueprints):
    """
    Registers blueprints with the app.
    """
    # Register blueprints.
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

def set_before_handlers(app, before_handlers):
    """
    Sets before handlers.
    """
    # Register before request middlewares.
    for before in before_handlers:
        before = app.before_request(before)

def set_after_handlers(app, after_handlers):
    """
    Sets after handlers.
    """
    # Register before request middlewares.
    for after in after_handlers:
        after = app.after_request(after)

def set_log_handlers(app, log_handlers):
    """
    Sets log handlers for the app.
    """
    # Set log handlers.
    for handler in log_handlers:
        app.logger.addHandler(handler)

def set_template_filters(app, template_filters):
    """
    Sets jinja2 template filters.
    """
    for filter_name, filter_fn in template_filters:
        app.jinja_env.filters[filter_name] = filter_fn

def set_context_processors(app, context_processors):
    """
    Sets jinja2 context processors.
    """
    for fn in context_processors:
        fn = app.context_processor(fn)

if __name__ == '__main__':
    #: Create the `app` object via :func:`init`. Run the `app`
    #: if called standalone.
    app = init()
    app.run()
