"""
Sets the mapping between `url_endpoints` and `view functions`.
"""
from werkzeug import import_string
from flask import Blueprint

routes = [
    'app.views.hello',
    ('/hello', 'hello', 'hello', {}),
]

pluggable_views = [
    'app.views.pluggable',
    ('/pluggable', 'pluggable', ('Pluggable', dict(template_name='hello.html')), {}),
    ('/restful', 'restful', ('Restful', dict(template_name='hello.html')), {}),
]

def set_urls(app):
    """
    Connects url patterns to actions for the given wsgi `app`.
    """
    _set_routes(app)
    _set_pluggable_views(app)

def _set_routes(app):
    """
    Sets module urls.
    """
    for rule in routes:
        if isinstance(rule, str):
            _set_routes.module = import_string(rule)
            # Register blueprint.
            _register_blueprint(app, rule)
            continue
        # Set url rule.
        url_rule, endpoint, view_func, opts = rule
        view_func = getattr(_set_routes.module, view_func)
        app.add_url_rule(url_rule, endpoint=endpoint,
                         view_func=view_func, **opts)
_set_routes.module = None

def _set_pluggable_views(app):
    """
    Sets url rules for pluggable views.
    """
    for rule in pluggable_views:
        if isinstance(rule, str):
            _set_pluggable_views.module = import_string(rule)
            # Register blueprint.
            _register_blueprint(app, rule)
            continue
        # Set url rule.
        url_rule, endpoint, (view_class, kwargs), opts = rule
        view_func = getattr(_set_pluggable_views.module, view_class).as_view(endpoint, **kwargs)
        app.add_url_rule(url_rule, view_func=view_func, **opts)
_set_pluggable_views.module = None

def _register_blueprint(app, blueprint_path,
                        static_folder='static', template_folder='templates'):
    """
    Registers `blueprint` with the app.
    """
    blueprint_name = blueprint_path.split('.')[-1]
    if blueprint_name not in app.blueprints:
        blueprint = Blueprint(blueprint_name, blueprint_path,
                              static_folder='static',
                              template_folder='templates')
        app.register_blueprint(blueprint)
