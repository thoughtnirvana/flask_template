from fabric.api import local

def test():
    """
    Runs unit tests.
    """
    local('nosetests -v')

def deps_get():
    """
    Installs dependencies.
    """
    local("pip install -r reqs")

def deps_update():
    """
    Updates dependencies.
    """
    local("pip install -r reqs --upgrade")

def server():
    """
    Runs development server.
    """
    app = _make_app()
    app.run()

def run_tornado(port=8080):
    """
    Runs application under tornado.
    """
    import script.serve_app_tornado as runner
    _runner(runner, port)

def run_gevent(port=8080):
    """
    Runs gevent server.
    """
    import script.serve_app_gevent as runner
    _runner(runner, port)

def _runner(runner, *args, **kwargs):
    import werkzeug.serving
    import os
    environ = os.environ.get('FLASK_ENV')
    app = _make_app()
    if not environ or environ != 'prod':
        # Run with reloading.
        @werkzeug.serving.run_with_reloader
        def run_server():
            runner.run_server(app, *args, **kwargs)
        run_server()
    else:
        runner.run_server(app, *args, **kwargs)

def _make_app(basic_app=False):
    """
    Returns main wsgi app object.
    """
    import main
    return main.init(basic_app)
