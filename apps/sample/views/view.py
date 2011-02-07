# vim: set fileencoding=utf-8 :
# 3rd party imports.
from flask import g, request, render_template, flash, redirect, url_for
from flask import json, make_response, Response, abort
from flaskext.babel import lazy_gettext as _
# Project imports.
from ..models import User
from common.utils import set_trace
from shared import app

#: Derive the module name from the package name.
#: If the package name is `apps.admin.views.admin`, the
#: module name would be `admin`.
module_name = __name__.rsplit('.', 1)[1]
static_path = '/%s/static' % module_name

# Setting up error handlers.
# @app.errorhandler(httplib.NOT_FOUND)
# def error_handler(e):
#     return render_template('%s/404.html' % module_name,
#                            module_name=module_name,
#                            static_path=static_path), httplib.NOT_FOUND
# 

# Sample view function.
# def handle_login():
#     """
#     Login user. Calls relevant login method.
#     """
#     if request.method == 'POST':
#         # Handle FB registration.
#         if request.form.get('signed_request'):
#             return register()
#         # Handle login.
#         elif request.form.get('login'):
#             return login()
#     return render_template('%s/login.html' % module_name, module_name=module_name,
#                            static_path=static_path)
