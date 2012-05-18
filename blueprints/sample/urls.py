from .views import hello, test_ensure_args, Pluggable, Restful

routes = [
    ('/hello', hello),
    ('/test_ensure', test_ensure_args),
    ('/pluggable', Pluggable.as_view('pluggable', template_name='hello.html')),
    ('/restful', Restful.as_view('restful', template_name='hello.html')),
]
