from flask import render_template
from flask.views import View
from flask.views import MethodView

class Pluggable(View):
    def __init__(self, template_name):
        self.template_name = template_name

    def dispatch_request(self):
        return render_template(self.template_name)

class Restful(MethodView):
    def __init__(self, template_name):
        self.template_name = template_name

    def get(self):
        return render_template(self.template_name)
