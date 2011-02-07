"""
Sets the mapping between `url_endpoints` and `view functions`.
The `view_functions` are stored in the class:LazyView and are
loaded on demand. This lazy loading is crucial for appengine, as
it kills the applications every 5 minutes or so.
"""
#: 3rd party imports.
from flask import Module, g
from werkzeug import cached_property, import_string
#: Project imports
import shared

# Example
# routes = (
#     # User authentication and other user related stuff.
#     'apps.wordify.views.wordify',
#     ('/', 'init', 'init', {'methods': ['GET', 'POST']}),
#     ('/signup', 'signup', 'init', {'methods': ['GET', 'POST']}),
#     ('/<string(length=32):id>', 'user_wall', 'user_wall', {}),
# )


def set_urls(app):
    """
    Connects url patterns to actions for the given wsgi `app`.
    :class:`LazyView` is used as a proxy for view functions.
    It instantiates the actual view function when needed.
    """
    global routes
    for rule in routes:
        if isinstance(rule, str):
            set_urls.prefix = rule
            continue
        url_rule, endpoint, import_name, opts = rule
        #: Bind the `url_endpoint` to a :class:`LazyView`.
        full_import = '%s.%s' % (set_urls.prefix, import_name)
        view = LazyView(full_import)
        app.add_url_rule(url_rule, endpoint=endpoint,
                         view_func=view, **opts)
#: The `view function` prefix.
set_urls.prefix = ''


class LazyView(object):
    """
    Proxy for actual view. When called for an url pattern, it
    loads the module, registers it with `current_app` and returns
    the view function. The loading is of actual view function
    is cached.
    """

    def __init__(self, import_name):
        """
        Stores the `import_name` for further instantiation.
        """
        self.__module__, self.__name__ = import_name.rsplit('.', 1)
        self.import_name = import_name
        self.module_name = self.__module__.rsplit('.', 1)[1]

    @cached_property
    def view(self):
        """
        Cached proxy for actual `view function`. On first invocation,
        instantiates the stored `view function` and registers the
        corresponding `flask module`.
        """
        view_func = import_string(self.import_name)
        if self.module_name not in shared.app.modules:
            module = Module(self.__module__)
            shared.app.register_module(module)
        return view_func

    def __call__(self, *args, **kwargs):
        """
        When called, delegate to actual `view function`.
        """
        return self.view(*args, **kwargs)
