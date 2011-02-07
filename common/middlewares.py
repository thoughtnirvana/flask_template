class MethodRewriteMiddleware(object):
    """
    Middleware to handle RESTful requests from clients which
    don't support whole of REST (GET, PUT, POST, DELETE).

    The method name is passed as a form field and the request
    is re-written here.
    """
    def __init__(self, app, input_name='_method'):
        self.app = app
        self.input_name = input_name

    def __call__(self, environ, start_response):
        request = Request(environ)

        if self.input_name in request.form:
            method = request.form[self.input_name].upper()

            if method in ['GET', 'POST', 'PUT', 'DELETE']:
                environ['REQUEST_METHOD'] = method

        return self.app(environ, start_response)


