from flask.views import View
from flask.views import MethodView
from flask import render_template
from lib.flask_augment import check_args
from lib.flask_augment import ensure_args, ensure_presence

def hello():
    return render_template('hello.html')


class Pluggable(View):
    def __init__(self, template_name):
        self.template_name = template_name

    def dispatch_request(self):
        errors = check_args(a=(lambda x: x and int(x) > 10, 'Should be greater than 10.'))
        if errors: return str(errors)
        return render_template(self.template_name, name='pluggable')


class Restful(MethodView):
    def __init__(self, template_name):
        self.template_name = template_name

    def get(self):
        errors = check_args(a=(lambda x: x, 'Value must be provided.'))
        if errors: return str(errors)
        return render_template(self.template_name, name='restful')

@ensure_presence(token=1)
@ensure_args(a=(lambda x: x and (int(x) > 10), '"a" should be greater than 10'))
def test_ensure_args():
    return 'test'

def _test_ensure_args_handler(errors):
    return str(errors)

