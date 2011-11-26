"""
Sets the mapping between `url_endpoints` and `view functions`.
"""
from werkzeug import import_string
from flask import Blueprint

routes = [
    'app.views.hello',
    ('/hello', 'hello'),
    'app.views.pluggable',
    ('/pluggable', ('Pluggable', dict(template_name='hello.html'))),
    ('/restful', ('Restful', dict(template_name='hello.html'))),
]


def set_urls(app):
    """
    Connects url patterns to actions for the given wsgi `app`.
    """
    module = None
    blueprint = None
    for rule in routes:
        if isinstance(rule, str):
            # Register blueprint.
            if blueprint:
                if blueprint.name not in app.blueprints:
                    app.register_blueprint(blueprint)
            # New blueprint.
            blueprint_path = rule
            blueprint_name = blueprint_path.split('.')[-1]
            blueprint = Blueprint(blueprint_name, blueprint_path,
                                  static_folder='static',
                                  template_folder='templates')
            module = import_string(rule)
            continue
        # Set url rule.
        url_rule, endpoint, view_func, opts = _parse_rule(rule)
        view_func = _get_view_func(module, view_func, endpoint)
        blueprint.add_url_rule(url_rule, endpoint=endpoint,
                               view_func=view_func, **opts)
    # Register last blueprint.
    if blueprint and blueprint.name not in app.blueprints:
        app.register_blueprint(blueprint)

def _get_view_func(module, view_func, endpoint=None):
    """
    If `view_func` is a string, gets attribute `view_func` from `module`.
    If `view_func` is a 2-tuple, constructs pluggable view and returns it.
    """
    if isinstance(view_func, str):
        return getattr(module, view_func)
    view_class, kwargs = view_func
    view_class = getattr(module, view_class)
    endpoint = endpoint or view_class.__name__.lower()
    view_func = view_class.as_view(endpoint, **kwargs)
    return view_func

def _parse_rule(rule):
    """
    Breaks `rule` into `url`, `endpoint`, `view_func` and `opts`
    """
    length = len(rule)
    if length == 4:
        # No processing required.
        return rule
    elif length == 3:
        rule = list(rule)
        endpoint = None
        opts = {}
        if isinstance(rule[2], dict):
            # Options passed.
            opts = rule[2]
            view_func = rule[1]
        else:
            # Endpoint passed.
            endpoint = rule[1]
            view_func = rule[2]
        return (rule[0], endpoint, view_func, opts)
    elif length == 2:
        url_rule, view_func = rule
        return (url_rule, None, view_func, {})
    else:
        raise ValueError('URL rule format not proper %s' % (rule, ))
